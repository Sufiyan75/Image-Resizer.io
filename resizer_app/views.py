from django.shortcuts import render, HttpResponse
import PIL
from PIL import Image
import os
from django.contrib import messages
import zipfile

# Create your views here.
def index(requests):
    return render(requests, 'index.html')

def singleimage(request):
    if request.method == "POST":
        image1 = request.FILES['singleimg']
        resolution1 = request.POST.get('reso')
        format1 = request.POST.get('format')

        image_name = image1.name
        
        imagenm = os.path.splitext(image_name)[0]

        img = Image.open(image1)
        
        fileformat = format1

        newpath = 'static/compressed_img/' 
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        
        iurl = 'static/compressed_img/compressed_'

        try:
            if resolution1 == "High":
                img.save(f'{iurl}{imagenm}.{fileformat}', optimize=True, quality=50)
            elif resolution1 == "Medium":
                img.save(f'{iurl}{imagenm}.{fileformat}', optimize=True, quality=30)
            elif resolution1 == "Low":
                img.save(f'{iurl}{imagenm}.{fileformat}', optimize=True, quality=10)

            # Generate the file path of the compressed image
            compressed_image_path = f'{iurl}{imagenm}.{fileformat}'

            # Read the compressed image file as binary data
            with open(compressed_image_path, 'rb') as file:
                compressed_image_data = file.read()

            # Create a response with the compressed image data
            response = HttpResponse(content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{imagenm}.{fileformat}"'

            # Set the response content as the compressed image data
            response.content = compressed_image_data

            # Delete the compressed image file from the server
            os.remove(compressed_image_path)

            # Return the response to automatically download the compressed image
            return response
         
        except Exception as e:
            messages.warning(request, f'Something Went Wrong: {e}')
    return render(request, 'singleimage.html')

def multipleimage(request):
    if request.method == 'POST':
        files = request.FILES.getlist('singleimg')
        resolution1 = request.POST.get('reso')
        format1 = request.POST.get('format')

        # Get the names of the files
        for file in files:
            image_name = file.name

            imagenm = os.path.splitext(image_name)[0]

            img = Image.open(file)
            
            fileformat = format1

            newpath = 'static/compressed_folder/' 
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            
            iurl = 'static/compressed_folder/'

            try:
                if resolution1 == "High":
                    img.save(f'{iurl}{imagenm}.{fileformat}', optimize=True, quality=50)
                elif resolution1 == "Medium":
                    img.save(f'{iurl}{imagenm}.{fileformat}', optimize=True, quality=30)
                elif resolution1 == "Low":
                    img.save(f'{iurl}{imagenm}.{fileformat}', optimize=True, quality=10)
            except Exception as e:
                messages.warning(request, f'Something Went Wrong: {e}')
        

        folder_to_compress = 'static/compressed_folder'
        output_zip = 'static/zip_folder.zip'

        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_to_compress):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, folder_to_compress))
        
        zurl = 'static/'
        zimagenm = 'zip_folder'
        zfileformat = 'zip'

        #Generate the file path of the compressed image
        compressed_image_path = f'{zurl}{zimagenm}.{zfileformat}'

        # Read the compressed image file as binary data
        with open(compressed_image_path, 'rb') as file:
            compressed_image_data = file.read()

        # Create a response with the compressed image data
        response = HttpResponse(content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{zimagenm}.{zfileformat}"'

        # Set the response content as the compressed image data
        response.content = compressed_image_data

        # Delete the compressed image file from the server
        os.remove(compressed_image_path)


        def clear_folder(folder_path):
            # List all files in the folder
            files = os.listdir(folder_path)

            # Iterate over the files and delete them
            for file in files:
                file_path = os.path.join(folder_path, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        
        clear_folder(folder_to_compress)

        # Return the response to automatically download the compressed image
        return response
    return render(request, 'multipleimage.html')