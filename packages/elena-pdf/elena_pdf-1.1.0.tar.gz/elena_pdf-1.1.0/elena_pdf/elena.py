#! python3

import PyPDF2, os, sys, logging, pdf2image, img2pdf, send2trash
from PIL import Image 

class PdfManager (): 
    """
    Manage pdf files: merge, split convert pdff to img or convert img to pdfi
    """

    def __init__ (self, input_files = "", replace = False, debug = False):
        """
        Constructor of class. Generate empty list of files an get dir path and file ouput
        """

        # Debug configuration
        logging.basicConfig( level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s' )
        if not debug: 
            logging.disable()

        self.debug = debug
        self.pdfFiles = []
        self.imgFiles = []
        self.input_files = input_files
        self.output_file = ""
        
        self.replace = replace

        self.list_extensions = ["pdf", "jpg"]


        self.__verify_files()


    def __verify_files (self):
        """
        Varify that the files already exist in the local storage
        """

        # Convert only element to list 
        if type(self.input_files) == str: 
            file = self.input_files
            self.input_files = []
            self.input_files.append (file)

        # Loop for each file 
        for file in self.input_files: 
            
            # No found error
            if not os.path.isfile (file): 
                raise FileNotFoundError (file)

    def __verify_extension_input_files (self, pdf, function_name): 
        """ 
        Validate the extension of each file
        """

        # Generate a local list of extensions
        if pdf: 
            list_extensions = ["pdf"]
        else: 
            list_extensions = ["jpg"]


        # Loop for each file
        for file in self.input_files: 
            
            # Extension error
            extension_index = file.rfind (".")
            extension = file [extension_index + 1 :]

            if extension not in list_extensions: 
                raise AttributeError ("'{}'. \
                    \nFunction {} doesn't support the extension: '{}'" \
                    .format (file, function_name, extension))

    def __verify_output_file (self, file, default_name, extension): 
        """
        Verify the name of the output file and if the file will be replace or not
        """


        # verify path and make file name
        if os.path.isdir (file): 
            # Make the default file in the specific foder
            self.output_file = os.path.join(file, default_name + extension)
        elif file.endswith(extension):
            # Verify if the parent folder exist
            parent_path = os.path.dirname(file) 
            if os.path.isdir (parent_path): 
                # Make an specific file in specific folder
                self.output_file = file
            else: 
                message = 'Parent folder "{}" doesn\'t exist'.format (parent_path)
                raise ValueError(message)
        else:
            # Verify the path of the file          
            path_file = os.path.split (file)

            if path_file[0] == "": 
                # make file in current directory
                self.output_file = file + extension
            else: 
                # Verify if the parent folder exist
                parent_path = os.path.dirname(file) 
                if os.path.isdir (parent_path): 
                    # Make the file in the parent folder 
                    self.output_file = file + extension
                else: 
                    message = 'Parent folder "{}" doesn\'t exist'.format (parent_path)
                    raise ValueError(message)



        # Verify replace outputh file
        if os.path.isfile (self.output_file):
            if self.replace: 
                logging.debug ('Replacing file "{}"'.format (os.path.basename (self.output_file)))
            else: 
                message = 'File "{}" already exist'.format (self.output_file)
                raise ValueError(message)
    
    def __verify_output_folder (self, folder): 
        """
        Verify if output folder already exist. 
        If folder dosent exist, make it
        """

        # Verify if is folder
        if os.path.isfile (folder): 
            message = 'Error output folder. ({})\nThe output folder need to be a folder, not a file.'.format (folder)
            raise ValueError(message)
        elif folder.strip() == "":
            message = 'The function need a destination folder.'
            raise ValueError(message)
        elif not os.path.isdir (folder): 
            message = 'Output folder ({}), doesn\'t exist.'.format (folder)
            raise FileNotFoundError (message)



    def merge (self, merged_file): 
        """
        Merge a specific list of pdf files inside the output file
        """

        self.__verify_extension_input_files (pdf=True, function_name = "merge")

        self.__verify_output_file (merged_file, "merged_file", ".pdf")

        
        pdfWriter = PyPDF2.PdfFileWriter()

        # loop through all the pdf files
        if self.input_files: 
            for currentFile in self.input_files: 
                pdfFileObj = open (currentFile, 'rb')
                pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
                
                logging.debug ("Merging {}... ".format (currentFile))

                # loop through all the pages (except the first) and add them
                if pdfReader.numPages: 
                    for pageNum in range (0, pdfReader.numPages): 
                        pageObj = pdfReader.getPage(pageNum)
                        pdfWriter.addPage (pageObj)            
            
            # Save the resulting pdf to a file
            pdfOutput = open (self.output_file, 'wb')
            pdfWriter.write(pdfOutput)
            pdfOutput.close()

            logging.debug ('Done. Pages are now in "{}".'.format (self.output_file))
        else: 
            logging.debug ("List of files empty.")

    def split (self, output_folder, split_base_name = "-split-"): 
        """
        Split a specific list of pdf files inside specific folder
        """

        self.__verify_extension_input_files (pdf=True, function_name = "split")

        self.__verify_output_folder(output_folder)
        

        # loop through all the pdf files
        if self.input_files: 
            for currentFile in self.input_files: 
                pdfFileObj = open (currentFile, 'rb')
                pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
                
                logging.debug ("Dividing {}... ".format (currentFile))

                # loop through all the pages (except the first) and add them
                if pdfReader.numPages: 
                    for pageNum in range (0, pdfReader.numPages): 

                        # Save page of file, as new pdf file
                        pdfWriter = PyPDF2.PdfFileWriter()
                        pageObj = pdfReader.getPage(pageNum)
                        pdfWriter.addPage (pageObj)            

                        # Create the output file path
                        parent_file_name = os.path.basename (currentFile)
                        file_name = parent_file_name[:-4] + "{}{}.{}".format (split_base_name, str(pageNum + 1), "pdf")
                        file_path = os.path.join (output_folder, file_name)

                        # Verify if file exist
                        self.__verify_output_file (file_path, "", ".pdf") 

                        # Save file
                        pdfOutput = open (self.output_file, 'wb')
                        pdfWriter.write(pdfOutput)
                        pdfOutput.close()

                        logging.debug ('File "{}" generated.'.format (file_path))
                else: 
                    logging.debug ('File "{}" has not pages.'.format (file_name))

        else: 
            logging.debug ("List of files empty.")
    
    def pdf_to_img (self, output_folder, convert_base_name = "-img-"): 
        """
        Convert each page from pdf file(s), to jpg image
        """
 
        self.__verify_extension_input_files (pdf=True, function_name = "pdf_to_img")

        self.__verify_output_folder(output_folder)
        

        # loop through all the pdf files
        if self.input_files: 
            for currentFile in self.input_files: 
                
                logging.debug ("Converting {}... ".format (currentFile))

                # Store Pdf with convert_from_path function
                images = pdf2image.convert_from_path(currentFile)
                
                for i in range(len(images)):
                
                     # Create the output file path
                    parent_file_name = os.path.basename (currentFile)
                    file_name = parent_file_name[:-4] + "{}{}.{}".format (convert_base_name, str(i + 1), "jpg")
                    file_path = os.path.join (output_folder, file_name)

                    # Verify if file exist
                    self.__verify_output_file (file_path, "", ".jpg") 

                    # Save file
                    images[i].save(file_path)

                    logging.debug ('File "{}" generated.'.format (file_path))

        else: 
            logging.debug ("List of files empty.")


    def img_to_pdf (self, output_folder, merge_file=""): 
        """
        Convert list of images, to pdf files
        """

        self.__verify_extension_input_files (pdf=False, function_name = "img_to_pdf")

        self.__verify_output_folder(output_folder)
        

        # List of pdf files generated
        pdf_generated_files = []

        # loop through all the pdf files
        if self.input_files: 
            for currentFile in self.input_files: 
                
                logging.debug ("Converting {}... ".format (currentFile))


                # Create the output file path
                parent_file_name = os.path.basename (currentFile)

                # Get the position of the start of the extension
                ext_position = str(parent_file_name).rfind(".")

                file_name = parent_file_name[:ext_position] + ".pdf"
                file_path = os.path.join (output_folder, file_name)

                # Verify if file exist
                self.__verify_output_file (file_path, "", ".pdf") 

                # opening image 
                image = Image.open(currentFile) 
                
                # converting into chunks using img2pdf 
                pdf_bytes = img2pdf.convert(image.filename) 
                
                # opening or creating pdf file 
                file = open(file_path, "wb") 
                
                # writing pdf files with chunks 
                file.write(pdf_bytes) 
                
                # closing image file 
                image.close() 
                
                # closing pdf file 
                file.close() 

                # Add to list
                pdf_generated_files.append (file_path)

        else: 
            logging.debug ("List of files empty.")

        # Merge all generaterd files
        if merge_file: 
            if pdf_generated_files: 

                # Merge
                sub_pdf_manager = PdfManager (pdf_generated_files, self.replace, self.debug)
                sub_pdf_manager.merge (merge_file)

                # Delate individual files
                for pdf_file in pdf_generated_files: 
                    send2trash.send2trash (pdf_file)
