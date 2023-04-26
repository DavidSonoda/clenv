# Write a class that will load the index file and manage the profiles
# The class will have several methods to add, remove, and checkout profiles
# The class will also have a method to save the index file
# Basically this ConfigManager class will be having all the functionalities in the config_manager.py file
# But it's in a OOD way.
import json
import os
import re
import shutil
from pyhocon import ConfigFactory, HOCONConverter


class ConfigManager:
    def __init__(self, index_file_path, save_index=True):
        self.__index_file_path = index_file_path
        self.__EMPTY_INDEX_JSON = {"profiles": {"active": [], "non_active": []}}
        index_json = self.__load_index_file(index_file_path)
        self.__new_index_json = self.__refresh_index(index_json)
        if save_index:
            self.save_index()

    # Return a list of object, each object has 2 keys:
    # - profile_name
    # - file_path
    # The list should contain all the profiles in the index file, including the active profile
    # and the non-active profiles
    # Solution
    def get_all_profiles(self):
        return (
            self.__new_index_json["profiles"]["active"]
            + self.__new_index_json["profiles"]["non_active"]
        )

    # Get active profile. Return a list of object, each object has 2 keys:
    # - profile_name
    # - file_path
    def get_active_profile(self):
        return self.__new_index_json["profiles"]["active"]

    def get_non_active_profiles(self):
        return self.__new_index_json["profiles"]["non_active"]

    def get_profile(self, profile_name):
        for profile in (
            self.__new_index_json["profiles"]["active"]
            + self.__new_index_json["profiles"]["non_active"]
        ):
            if profile["profile_name"] == profile_name:
                return profile
        raise Exception(f"Profile {profile_name} does not exist")

    # Return a boolean value, True if there's at least one profile's name is 'default'
    def profile_has_initialized(self):
        for profile in (
            self.__new_index_json["profiles"]["active"]
            + self.__new_index_json["profiles"]["non_active"]
        ):
            if profile["profile_name"] == "untitled":
                return False
        return True

    # Rename a profile, the old_profile_name could be in both non_active and active list
    def rename_profile(self, old_profile_name, new_profile_name):
        for profile in (
            self.__new_index_json["profiles"]["active"]
            + self.__new_index_json["profiles"]["non_active"]
        ):
            if profile["profile_name"] == old_profile_name:
                profile["profile_name"] = new_profile_name
                # If the profile is active, do not rename the config file path
                # If the profile is non-active, rename the config file path
                if profile in self.__new_index_json["profiles"]["non_active"]:
                    new_file_path = os.path.expanduser(
                        profile["file_path"].replace(
                            f"clearml-{old_profile_name}.conf",
                            f"clearml-{new_profile_name}.conf",
                        )
                    )
                    os.rename(os.path.expanduser(profile["file_path"]), new_file_path)
                    profile["file_path"] = new_file_path
                self.save_index()
                return
        raise Exception(f"Profile {old_profile_name} does not exist")

    def initialize_profile(self, profile_name):
        self.rename_profile("untitled", profile_name)

    def is_active_profile(self, profile_name):
        return (
            profile_name
            == self.__new_index_json["profiles"]["active"][0]["profile_name"]
        )

    # Switch the active profile to the profile with the given profile_name, the profile_name must
    # be in the non_active list, if not, throw an exception
    # Solution
    def set_active_profile(self, profile_name):
        # Check if the profile_name is in the non_active list
        non_active_profile_list = self.__new_index_json["profiles"]["non_active"]
        active_profile_list = self.__new_index_json["profiles"]["active"]
        if profile_name == active_profile_list[0]["profile_name"]:
            raise Exception(f"Profile {profile_name} is already the active profile")
        for profile in non_active_profile_list:
            try:
                if profile["profile_name"] == profile_name:
                    # Firstly, add the active profile to the non_active list with updated file_path
                    # and also rename the config file name. For example, if the active profile is 'default',
                    # then rename the config file name from 'clearml.conf' to 'clearml-default.conf'
                    # Remove the active profile from the active list
                    active_profile = self.__new_index_json["profiles"]["active"][0]
                    old_active_fp = active_profile["file_path"]
                    active_profile["file_path"] = active_profile["file_path"].replace(
                        "clearml.conf", f'clearml-{active_profile["profile_name"]}.conf'
                    )
                    self.__new_index_json["profiles"]["non_active"].append(
                        active_profile
                    )
                    self.__new_index_json["profiles"]["active"].remove(active_profile)
                    os.rename(
                        os.path.expanduser(old_active_fp),
                        os.path.expanduser(active_profile["file_path"]),
                    )

                    # Secondly, add the matching non-active profile to the active list with updated file_path
                    # and also rename the config file name. For example, if the non-active profile is 'dev',
                    # then rename the config file name from 'clearml-dev.conf' to 'clearml.conf'
                    # Remove the matching non-active profile from the non-active list
                    self.__new_index_json["profiles"]["non_active"].remove(profile)
                    old_inactive_fp = profile["file_path"]
                    profile["file_path"] = profile["file_path"].replace(
                        f"clearml-{profile_name}.conf", "clearml.conf"
                    )
                    os.rename(
                        os.path.expanduser(old_inactive_fp),
                        os.path.expanduser(profile["file_path"]),
                    )
                    self.__new_index_json["profiles"]["active"].append(profile)
                    self.save_index()
                    return
            except:
                raise
        raise Exception(f"Profile {profile_name} does not exist")

    # Create a new profile based on the given profile_name, the profile_name must not be in the
    # active list or the non_active list, if it is, throw an exception
    # Solution
    def create_profile(self, profile_name, base_profile_name=None):
        if self.has_profile(profile_name):
            raise Exception(f"Profile {profile_name} already exists")
        new_profile = {
            "profile_name": profile_name,
            "file_path": os.path.expanduser(f"~/clearml-{profile_name}.conf"),
        }
        self.__new_index_json["profiles"]["non_active"].append(new_profile)
        # Copy the config file specified by base_profile_name and rename it to the file_path

        if base_profile_name is None:
            base_profile_name = self.get_active_profile()[0]["profile_name"]
        base_profile = self.get_profile(base_profile_name)
        shutil.copyfile(
            os.path.expanduser(base_profile["file_path"]),
            os.path.expanduser(new_profile["file_path"]),
        )

        self.save_index()

    # Delete the profile with the given profile_name, the profile_name must be in the
    # active list or the non_active list, if it is not, throw an exception
    # Solution
    def delete_profile(self, profile_name):
        if not self.has_profile(profile_name):
            raise Exception(f"Profile {profile_name} does not exist")
        for profile in (
            self.__new_index_json["profiles"]["active"]
            + self.__new_index_json["profiles"]["non_active"]
        ):
            if profile["profile_name"] == profile_name:
                self.__new_index_json["profiles"]["non_active"].remove(profile)
                os.remove(os.path.expanduser(profile["file_path"]))
                self.save_index()
                return

    def has_profile(self, profile_name):
        for profile in (
            self.__new_index_json["profiles"]["active"]
            + self.__new_index_json["profiles"]["non_active"]
        ):
            if profile["profile_name"] == profile_name:
                return True
        return False

    def save_index(self):
        with open(os.path.expanduser(self.__index_file_path), "w") as f:
            f.write(json.dumps(self.__new_index_json, indent=4))

    # Reinitialize the api part of the config file of a specific profile, make sure the api_config
    # is a a valid hocon format string using pyhocon. Then replace the 'api' section of the config file
    # with the api_config
    def reinitialize_api_config(self, profile_name, api_config_str):
        if not self.has_profile(profile_name):
            raise Exception(f"Profile {profile_name} does not exist")
        try:
            profile = self.get_profile(profile_name)
            clearml_config = ConfigFactory.parse_file(
                os.path.expanduser(profile["file_path"])
            )
            new_api_config = ConfigFactory.parse_string(api_config_str)
            clearml_config["api"] = new_api_config["api"]
            with open(os.path.expanduser(profile["file_path"]), "w") as f:
                f.write(HOCONConverter.convert(clearml_config))
        except:
            raise Exception("Invalid api_config_str")

    def __refresh_index(self, index_json):
        # Scan the home directory
        new_index_json = self.__scan_home_dir()
        # If the default profile in index_json is not empty, update the new_index_json with the default profile
        # in index_json
        if len(index_json["profiles"]["active"]) > 0:
            new_index_json["profiles"]["active"] = index_json["profiles"]["active"]
        return new_index_json

    # Load the json content of the index file, return the json object. If the file
    # is empty or malformed, return an empty json object.
    def __load_index_file(self, file_path):
        index_file = os.path.expanduser(file_path)
        if not os.path.exists(index_file) or os.stat(index_file).st_size == 0:
            # return an empty json object
            return self.__EMPTY_INDEX_JSON
        else:
            try:
                with open(index_file, "r") as f:
                    return json.load(f)
            except:
                return self.__EMPTY_INDEX_JSON

    # Scan the home directory for files that match the criteria:
    # - the file name ends with .conf
    # - the file is not a directory
    # - the file is not a symbolic link
    # - the file name contains the word clearml
    # - the file content is in hocon format, using pyhocon library to detect if it is hocon format, throw
    #   an exception if it is not hocon format
    # Create a json object for each file, it got 2 keys
    # - profile name
    # - file path
    #
    # Return a list of json objects. Do not read the index file, just scan the home directory.
    #
    # Solution
    def __scan_home_dir(self):
        home_dir = os.path.expanduser("~")
        files = os.listdir(home_dir)
        active_profile_list = []
        non_active_profile_list = []
        for file in files:
            if (
                file.endswith(".conf")
                and not os.path.isdir(file)
                and not os.path.islink(file)
                and "clearml" in file
            ):
                try:
                    ConfigFactory.parse_file(f"{home_dir}/{file}")
                    if file == "clearml.conf":
                        active_profile_list.append(
                            {
                                "profile_name": self.__extract_profile_name(file),
                                "file_path": f"{home_dir}/{file}",
                            }
                        )
                    else:
                        non_active_profile_list.append(
                            {
                                "profile_name": self.__extract_profile_name(file),
                                "file_path": f"{home_dir}/{file}",
                            }
                        )
                except:
                    # throw an error
                    raise Exception(
                        f"Not a valid config file: {file}, check file content"
                    )

        return {
            "profiles": {
                "active": active_profile_list,
                "non_active": non_active_profile_list,
            }
        }

    # Extract profile name from the file name, if the file name is clearml.conf, the profile name should be default
    # If the file name is clearml-<profile_name>.conf, the profile name should be <profile_name>
    # Use regex to extract the profile name
    # Solution
    def __extract_profile_name(self, file_name):
        if file_name == "clearml.conf":
            return "untitled"
        else:
            return re.match(r"clearml-(.+)\.conf", file_name).group(1)
