import csv
import os
from PIL import Image
from django.core.management.base import BaseCommand
from application.models import *

class Command(BaseCommand):
    help = 'Imports data from a CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        with open(csv_file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row if it exists

            folder_path = 'C:\\Users\\admin\Work\\Code\\Plant_Project\\plantDatabase\\application\\media\\image'
            folders = sorted(os.listdir(folder_path), key=lambda x: int(x))
    

            for row, folder in zip(reader, folders):
                family_name_list = row[2].split(',')
                common_name_list =  row[3].split(',')
                
                new_instance = plant.objects.create(name=row[0],scientificName=row[1],uses=row[4]
                                                    ,characteristic=row[5],habitat=row[6],distribution=row[7]
                                                    ,care=row[8],location=row[9],references=row[10])
                new_instance.save()

                commonName_instance_list = []
                familyName_instance_list = []

                for name in family_name_list:
                    familyName_related_instance, familyName_create = familyName.objects.get_or_create(familyName=name)
                    familyName_instance_list.append(familyName_related_instance)

                for name in common_name_list:
                    commonName_related_instance , commonName_create = commonName.objects.get_or_create(commonName=name) 
                    commonName_instance_list.append(commonName_related_instance)
               
                new_instance.familyNameList.add(*familyName_instance_list)
                new_instance.commonNameList.add(*commonName_instance_list)

                print(folder)

                folder_image_path = os.path.join(folder_path, folder)
                for root, dirs, files in os.walk(folder_image_path):
                    image_instance_list = []
                    for file in files:
                         if file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                            file_path = os.path.join(root, file)
                            image_related_instance , image_create = plantImage.objects.get_or_create(image=file_path)
                            image_instance_list.append(image_related_instance)
                    
                    new_instance.plantImageList.add(*image_instance_list)

                            

                

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))