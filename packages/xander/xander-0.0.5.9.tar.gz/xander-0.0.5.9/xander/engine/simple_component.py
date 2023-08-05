class Component:
    """
    Basic execution component in the pipeline. It takes the input, runs the methods passed as parameter and returns
    the output that will be exported by the pipeline.
    """

    def __init__(self, slug, function, function_params, storage_manager, return_output=False):
        """
        Class constructor.

        @param name: name of the component
        @param function: function passed by the user that will be executed by the component (Python method)
        @param function_params: input parameters of the function (tuple)
        @param storage_manager: storage manager to retrieve files if needed and exports output
        @param return_output: if set to True the output of the component is returned to the pipeline instead of saved
                              in the storage
        @param logger: logger manager
        """

        self.slug = slug
        self.function = function
        self.params = function_params
        self.storage_manager = storage_manager
        self.return_output = return_output

    def run(self, *args):
        """
        Execute the component running the function with the specified parameters.
        The output is return to eventually passed to other components and it is saved in the storage.

        @return:
        """

        # List of params
        params_list = []

        # For each parameter provided by the user, the component puts in the params list or load it from the storage.
        for type, params in self.params:

            # File case
            if type == 'file':
                params_list.append(self.storage_manager.get_file(filename=params))

            # Folder case
            elif type == 'folder':
                params_list.append(self.storage_manager.get_folder_files(filename=params))

            # All other cases
            else:
                params_list.append(params)

        # If the list of components is not None, they are added to the params list
        added_arguments = list(args)
        if added_arguments:
            params_list.extend([a for a in added_arguments if a])

        # Run the component function
        outputs = self.function(*params_list)

        # If return output is disabled all outputs are saved in the storage
        if not self.return_output:
            self.storage_manager.export(outputs, self.slug)

        return None
