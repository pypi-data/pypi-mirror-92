import datetime
import os
import uuid
from time import sleep

from xander.engine.simple_component import Component


class Pipeline:

    def __init__(self, name, logger, storage_manager, client):

        # Unique identifier of the pipeline.
        self.pipeline_id = uuid.uuid4().hex

        # Name of the pipeline provided by the user.
        self.pipeline_name = name

        # Slug of the pipeline to better represent it in the system.
        self.pipeline_slug = '_'.join(self.pipeline_name.split(' ')).lower()

        # List of methods to be applied in the pipeline. If the pipeline performs correctly they are saved and reloaded
        # on cold start.
        self.components = []

        # Logger manager, it can be None
        self.logger = logger

        # Storage manager
        self.storage_manager = storage_manager
        self.storage_manager.create_sub_destination_folder(self.pipeline_slug, self.pipeline_slug)

        # Xander client
        self.client = client

        # Stats and numbers
        self.start_time = None
        self.end_time = None
        self.run_duration = None

    def run(self):
        """
        Run the pipeline using all specified methods.

        :return: True if the execution has terminated successfully, otherwise False.
        """

        # List of outputs, updated at each iteration

        start = datetime.datetime.now()

        # Update start time and push the change on the cloud server
        self.start_time = start.strftime('%Y-%m-%d %H:%M:%S')
        self.client.save_pipeline(pipeline=self)

        outputs = None

        for i, component in enumerate(self.components):
            self.logger.info("{}: component {}/{}".format(self.pipeline_slug, i + 1, len(self.components)))

            try:
                # The output of the previous component is passed to the current component, if the content is None or
                # non-needed nothing happens. The execution goes on.
                outputs = component.run(outputs)

            except ValueError as v:
                # Case in which the output is formatted wrongly by the user
                self.logger.critical(v)

        # Update end time
        end = datetime.datetime.now()
        self.end_time = end.strftime('%Y-%m-%d %H:%M:%S')

        # Update delta time and push the change on the cloud server
        delta = end - start
        self.run_duration = delta.seconds if delta.seconds > 0 else 1
        self.client.save_pipeline(pipeline=self)

        return True

    def add_component(self, name, function, function_params, return_output=None):
        """
        Add a new component to the pipeline.

        @param name: name of the component
        @param function: function to be executed
        @param function_params: input params for the function
        @param return_output: flag that indicates if the output is passed to the next component

        @return: True
        """

        # Compute the slug
        slug = name.lower().replace(' ', '_')

        # Initialize the new component
        component = Component(slug=slug, function=function, function_params=function_params,
                              storage_manager=self.storage_manager, return_output=return_output)

        # Add a folder for the component in the pipeline directory
        self.storage_manager.create_sub_destination_folder(os.path.join(self.pipeline_slug, slug), slug)

        # Add the component
        self.components.append(component)

        self.logger.info('Pipeline {} -> new component added.'.format(self.pipeline_slug))
        return True
