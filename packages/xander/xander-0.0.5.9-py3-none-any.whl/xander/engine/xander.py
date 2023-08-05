import datetime
import json
from uuid import uuid4

from xander.client.client import XanderClient, START_TIME, END_TIME, DURATION, PIPELINES, RUN_ID
from xander.engine.pipeline import Pipeline
from xander.engine.storage_manager import StorageManager
from xander.utils.logger import Logger


class XanderEngine:
    """
    The core of ML OPS tool.
    It is the object to be initialized by the user.
    """

    def __init__(self, local_source, local_destination, api_auth_file='zoe_sapphire.json', local_mode=False):
        """
        Class constructor.

        :param local_source: source folder in the local device
        :param local_destination: destination folder in the local device
        :param api_auth_file: authentication file to connect to cloud server
        """

        # Initialize the log manager
        self.logger = Logger()

        # Execution info
        self.execution = {
            RUN_ID: None,
            START_TIME: None,
            END_TIME: None,
            DURATION: 0,
            PIPELINES: 0
        }

        self.client = XanderClient(api_auth_file=api_auth_file, logger=self.logger, local_mode=local_mode)

        # Connect the client
        self.client.connect()

        self.logger.success('Zoe ML Engine is ready.')

        # Initialize the storage manager
        self.storage_manager = StorageManager(local_source=local_source, local_destination=local_destination,
                                              logger=self.logger)

        # Initialize the pipelines list
        self.pipelines = []

    def run(self):
        """
        Run the engine. All pipelines are executed with their components.

        @return: None
        """

        # Generate a new Run ID
        self.execution[RUN_ID] = uuid4().hex
        self.execution[START_TIME] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.execution[PIPELINES] = len(self.pipelines)
        self.client.save_run(self.execution)

        self.logger.success("Terna ML Engine is running.")

        for i, pipeline in enumerate(self.pipelines):

            self.logger.info("({}/{}) Running '{}'".format(i + 1, len(self.pipelines), pipeline.pipeline_slug))

            # Run pipeline
            pipeline.run()

            # Update duration time of the execution
            self.execution[DURATION] += pipeline.run_duration

            # Push the change on the cloud server
            self.client.save_run(self.execution)

            self.logger.info("Completed '{}'.".format(pipeline.pipeline_slug))


        # Update the end time
        self.execution[END_TIME] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Push the end of the execution on the server
        self.client.save_run(self.execution)
        self.logger.success("Terna ML Engine has terminated successfully.")

    def add_pipeline(self, name):
        """
        Add a new pipeline to the engine.

        @param name: name of the pipeline
        @return: the created pipeline
        """

        # Initialize the pipeline
        p = Pipeline(name=name, logger=self.logger, storage_manager=self.storage_manager, client=self.client)

        # Add the pipeline to the list to be executed
        self.pipelines.append(p)

        self.logger.info("Pipeline '{}' added to the engine".format(p.pipeline_name))

        # Return the pipeline
        return p
