#
# Author: Panagiotis Chartas (t3l3machus) 
#
# This script is part of the "Villain C2 Framework": 
# https://github.com/t3l3machus/Villain

import os

from .common import system_type
from .settings import Logging_Settings

main_meta_folder = Logging_Settings.main_meta_folder_unix if system_type in ['Linux', 'Darwin'] else Logging_Settings.main_meta_folder_windows


class HoaxShell_Implants_Logger:

    generated_implants_file = f'{main_meta_folder}/hoaxshell_generated_implants.txt'
    generated_implants_file_open = False


    @staticmethod
    def store_session_details(id, session_meta):

        try:

            while HoaxShell_Implants_Logger.generated_implants_file_open:
                pass

            HoaxShell_Implants_Logger.generated_implants_file_open = True
            with open(HoaxShell_Implants_Logger.generated_implants_file, 'a') as hoaxshell_generated_implants:
                hoaxshell_generated_implants.write(f'"{id}" : {session_meta!s}' + ',\n')
            HoaxShell_Implants_Logger.generated_implants_file_open = False

        except BaseException:  # noqa: BLE001, S110
            pass



    @staticmethod
    def retrieve_past_sessions_data():

        if os.path.exists(HoaxShell_Implants_Logger.generated_implants_file):

            try:

                while HoaxShell_Implants_Logger.generated_implants_file_open:
                    pass

                HoaxShell_Implants_Logger.generated_implants_file_open = True
                with open(HoaxShell_Implants_Logger.generated_implants_file, 'r') as hoaxshell_generated_implants:
                    session_data = hoaxshell_generated_implants.read()
                HoaxShell_Implants_Logger.generated_implants_file_open = False
                return '{' + session_data.strip(',\n') + '}'

            except Exception as e:  # noqa: BLE001
                print(e)
        
        return False
            


def clear_metadata():

    try:
        if os.path.exists(HoaxShell_Implants_Logger.generated_implants_file):
            os.remove(HoaxShell_Implants_Logger.generated_implants_file)
    except BaseException:  # noqa: BLE001
        return False
    
    return True



# Create folder to store logs and metadata
if os.path.exists(main_meta_folder):
    pass
else:
    os.makedirs(main_meta_folder)
