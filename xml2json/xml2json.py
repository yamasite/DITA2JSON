#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


import xml.etree.ElementTree as ET
import json
from os import path
import os

import sys

# ------------------------------------------------------
# Parse the dita file to get information. Child's play.
# ------------------------------------------------------

# TODO: !!!!!!!!!!!!!!!!!!!!!!!!!  Set your working path here !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
working_dir = 'C:\\Users\\WL\\Documents\\GitHub\\doc_source\\en-US\\dita\\RTC'

# working_dir = 'C:\\Users\\WL\\Documents\\GitHub\\doc_source\\dita\\RTC'
file_dir = ''

# TODO: !!!!!!!!!!!!!!!!!!!!!!!!!  Set your PLATFORM TAG here !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
platform_tag = "cpp"

# TODO: !!!!!!!!!!!!!!!!!!!!!!!!!  Set your JSON path here !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
json_file = "cpp_interface_new.json"

# TODO: !!!!!!!!!!!!!!!!!!!!!!!!!  Set your SDK here !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
sdk_type = "rtc-ng"
remove_sdk_type = "rtc"

# Get path of ditamap files that contain refs
# These variables are used globally
# android_path, cpp_path, rust_full_path, electron_path
android_path = "config/keys-rtc-api-android.ditamap"
cpp_path = "config/keys-rtc-api-cpp.ditamap"
rust_path = "config/keys-rtc-api-rust.ditamap"
electron_path = "config/keys-rtc-api-electron.ditamap"
c_sharp_path = "config/keys-rtc-api-unity.ditamap"

if sys.platform == 'darwin':
    print("macOS")
    android_full_path = path.join(working_dir, android_path)
    cpp_full_path = path.join(working_dir, cpp_path)
    rust_full_path = path.join(working_dir, rust_path)
    electron_full_path = path.join(working_dir, electron_path)
    c_sharp_path = path.join(working_dir, c_sharp_path)
    # Need to add electron??
elif sys.platform == 'win32':
    print("Windows")
    android_full_path = path.join(working_dir, android_path.replace("/", "\\"))
    cpp_full_path = path.join(working_dir, cpp_path.replace("/", "\\"))
    rust_full_path = path.join(working_dir, rust_path.replace("/", "\\"))
    electron_full_path = path.join(working_dir, electron_path.replace("/", "\\"))
    c_sharp_full_path = path.join(working_dir, c_sharp_path.replace("/", "\\"))
    # Need to add electron??

print(android_full_path)
print(cpp_full_path)
print(rust_full_path)
print(electron_full_path)
print(c_sharp_full_path)

# TODO: !!!!!!!!!!!!!!!!!!!!!!!!!  Set your defined path here !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# defined_path = electron_full_path
# defined_path = android_full_path
defined_path = cpp_full_path
# defined_path = c_sharp_full_path

# rust_full_path
# cpp_full_path
# Other types of full path
rust_topicref_list = []
dita_file_tree = ET.parse(defined_path)
dita_file_root = dita_file_tree.getroot()
for topicref in dita_file_root.iter("keydef"):
    print(topicref)
    if topicref.get("href") is not None:
        path_new = path.basename(topicref.get("href"))
        print(path_new)
        rust_topicref_list.append(path_new)

print("--------------- Topic ref list ------------------------")
print(rust_topicref_list)
print("--------------- Topic ref list ------------------------")

# Target platform

# List of platforms
props_platform_list = ["windows", "rust", "java", "python", "csharp", "objectivec"]


def create_json_from_xml(working_dir, file_dir, android_path, cpp_path, rust_path, platform="rust"):
    tree = ET.parse(file_dir)
    root = tree.getroot()

    # Iterate over all dita files
    #
    # --------------------------------------------------------------------------------------------------------------------
    # Replace xref -> keyrefs with actual names
    # For example:
    # <xref keyref="setClientRole"/>
    # ------------------------------------------------------------------------------------------------------------------------
    # for xref in root.iter("xref"):
    #     # print(xref.get("keyref"))
    #     if xref.get("keyref") is not None:
    #         xref.text = str(xref.get("keyref"))
    #         # ET.SubElement(xref, "text")
    # -----------------------------------------------------------------------------------------------------------------------------
    # Wow Wow
    # Pre-process the files to make sure that tags with props = "" in which the value is not consistent with the current platform
    # For example, if the current platform is "rust", and we have values in props other than "rust", the whole tag will be removed.
    # Currently hard-coded to rust. Will have more in the long run.
    #
    # There's no direct support in the form of a parent attribute, but you can perhaps use the patterns described here to achieve the desired effect.
    # The following one-liner is suggested (updated from the linked-to post to Python 3.8) to create a child-to-parent mapping for a whole tree,
    # using the method xml.etree.ElementTree.Element.iter:
    #
    # parent_map = {c: p for p in tree.iter() for c in p}
    parent_map = {c: p for p in tree.iter() for c in p}
    for child in root.iter('*'):
        if child.get("props") is not None:
            if platform_tag not in child.get("props") or remove_sdk_type in child.get("props"):
                print("------------------- Tag to remove ---------------------------")
                print(child)
                print(child.text)
                print("--------------------Tag to remove ---------------------------")
                parent_map[child].remove(child)
    #
    # ----------------------------------------------------------------------------
    # Implement all conrefs with the actual content
    # For example:
    # <p conref="../conref/conref_rtc_api.dita#apidef/onClientRoleChanged"> </p>
    # Depends on the relative location of conref
    # ----------------------------------------------------------------------------
    for child in root.iter('*'):
        if child.get("conref") is not None:
            conref = str(child.get("conref"))
            conref = conref.split("#")
            if "../" in str(conref[0]):
                new_working_dir = path.normpath(working_dir)
                # print(new_working_dir[0])
                # print(conref[0].replace("../", ""))
            if sys.platform == 'darwin':
                print("macOS")
                conref_path = path.join(new_working_dir, str(conref[0]).replace("../", ""))
            elif sys.platform == 'win32':
                print("Windows")
                conref_path = path.join(new_working_dir, str(conref[0]).replace("../", "").replace("/", "\\"))
            print(" ---------------------- Get the conref path ----------------------------")
            print(conref_path)
            print(" ---------------------- Get the conref path ----------------------------")
            # ---------------------------------------------------------------------------------------------------
            # Read the referenced dita file and get the content
            # ---------------------------------------------------------------------------------------------------
            dita_file_tree = ET.parse(conref_path)
            dita_file_root = dita_file_tree.getroot()
            print(str(conref[1]))

            xpath_list = str(conref[1]).split("/")
            last_id = xpath_list[-1]
            # Get the last ID
            print(" ---------------------- Last ID ----------------------------")
            print(last_id)
            print(" ---------------------- Last ID ----------------------------")

            # Find tag by id
            dita_ref_text = ""
            for dita_tag in dita_file_root.iter('*'):
                # print(str(dita_tag.get("id")))
                # print(last_id)
                if dita_tag is not None:
                    if str(dita_tag.get("id")) == str(last_id):
                        print(dita_tag)
                        for tag in dita_tag.iter():
                            print(tag)
                            dita_ref_text = dita_ref_text + dita_tag.text

            print("------------------- Dita ref text -----------------------")
            print(dita_ref_text)
            print("------------------- Dita ref text -----------------------")

            # Inject text to the original conref
            child.text = dita_ref_text
            print("------------------- Final change -----------------------")
            print(child.text)
            print("------------------- Final change -----------------------")

    # ----------------------------------------------------------------------------
    #     # Implement all conkeyrefs with the actual content
    #     # For example:
    #     # <ph conkeyref="createAgoraRtcEngine1/shortdesc"/>
    #     # It is first a keyref then a conref
    #     # Conkeyrefs should be replaced at the element level!!!!!!!!!
    # ----------------------------------------------------------------------------
    for child in root.iter('*'):
        if child.get("conkeyref") is not None:
            conkeyref = str(child.get("conkeyref"))
            print("Conkeyref is " + conkeyref)
            conkeyref_array = conkeyref.split("/")
            # key
            key = conkeyref_array[0]
            # ref
            ref = conkeyref_array[1]
            # Assume that a conkeyref contains only two levels
            dita_file_tree = ET.parse(defined_path)
            dita_file_root = dita_file_tree.getroot()
            for keydef in dita_file_root.iter("keydef"):
                if keydef.get("keys") == key:
                    href_text = keydef.get("href")
                else:
                    href_text = ""
            print("----------------------href text--------------------")
            print(href_text)
            print("----------------------href text--------------------")

            final_parent = child

            # Get the parent old child
            for parent in root.iter('*'):
                for d in parent.iterfind(child.tag):
                    if d is child:
                        final_parent = parent

            if sys.platform == 'darwin':
                print("macOS")
                if href_text is not None and href_text != "":
                    dir = path.join(working_dir, href_text).replace("../", "")
                else:
                    dir = None
            elif sys.platform == 'win32':
                print("Windows")
                if href_text is not None and href_text != "":
                    dir = path.join(working_dir, href_text).replace("../", "").replace("/", "\\")
                else:
                    dir = None
            if dir is not None:
                print(dir)
                new_dita_file_tree = ET.parse(dir)
                new_dita_file_root = new_dita_file_tree.getroot()
                # Find the keyref
                for new_child in new_dita_file_root.iter('*'):
                    if new_child.get("id") == ref:
                        print("------------ Found a match for conkeyref -----------------")
                        print(ref)
                        print("------------ Found a match for conkeyref-----------------")
                        # Set the node from new child to old child
                        final_parent.insert(0, new_child)
                        final_parent.remove(child)

                print("----------------------conkeyref text--------------------")
                print(child)
                print("----------------------conkeyref text--------------------")

    # Do it twice
    for child in root.iter('*'):
        if child.get("conkeyref") is not None:
            conkeyref = str(child.get("conkeyref"))
            print("Conkeyref is " + conkeyref)
            conkeyref_array = conkeyref.split("/")
            # key
            key = conkeyref_array[0]
            # ref
            ref = conkeyref_array[1]
            # Assume that a conkeyref contains only two levels
            dita_file_tree = ET.parse(defined_path)
            dita_file_root = dita_file_tree.getroot()
            for keydef in dita_file_root.iter("keydef"):
                if keydef.get("keys") == key:
                    href_text = keydef.get("href")
            print("----------------------href text--------------------")
            print(href_text)
            print("----------------------href text--------------------")

            final_parent = child

            # Get the parent old child
            for parent in root.iter('*'):
                for d in parent.iterfind(child.tag):
                    if d is child:
                        final_parent = parent

            if sys.platform == 'darwin':
                print("macOS")
                if href_text is not None and href_text != "":
                    dir = path.join(working_dir, href_text).replace("../", "")
                else:
                    dir = None
            elif sys.platform == 'win32':
                print("Windows")
                if href_text is not None and href_text != "":
                    dir = path.join(working_dir, href_text).replace("../", "").replace("/", "\\")
                else:
                    dir = None
            if dir is not None:
                print(dir)
                new_dita_file_tree = ET.parse(dir)
                new_dita_file_root = new_dita_file_tree.getroot()
                # Find the keyref
                for new_child in new_dita_file_root.iter('*'):
                    if new_child.get("id") == ref:
                        print("------------ Found a match for conkeyref -----------------")
                        print(ref)
                        print("------------ Found a match for conkeyref-----------------")
                        # Set the node from new child to old child
                        final_parent.insert(0, new_child)
                        final_parent.remove(child)

                print("----------------------conkeyref text--------------------")
                print(child)
                print("----------------------conkeyref text--------------------")

    # TODO: Implement API name keyrefs
    # Tags can be like <apiname keyref="addInjectStreamUrl"/> and <xref keyref="setChannelProfile"/>
    # The keys are defined in ditamap files such as:
    # Android: ../config/keys-rtc-api-android.ditamap
    # CPP: ../config/keys-rtc-api-cpp.ditamap
    # Rust: ../config/keys-rtc-api-rust.ditamap
    # ---------------------------------------------------------------------------
    # TODO: Use args to determine the platform
    # -- android
    # -- cpp
    # -- rust
    # ...
    # ---------------------------------------------------------------------------

    # Get keyword from keydef in ditamap files
    #     <keydef keys="onClientRoleChanged" href="../API/onClientRoleChanged.dita">
    #         <topicmeta>
    #             <keywords>
    #                 <keyword>onClientRoleChanged</keyword>
    #             </keywords>
    #         </topicmeta>
    #     </keydef>
    #
    #
    #
    # <apiname keyref="addInjectStreamUrl"/> for each API category
    #
    # CPP
    for apiname in root.iter("apiname"):
        # print(xref.get("keyref"))
        # For each xref, perform the following operations:
        # 1. Get the ditamap file per platform
        # 2. Extract href text from ditamap
        # 3. Set href text in current dita
        href_text = ""
        if apiname.get("keyref") is not None:
            # xref.text = str(xref.get("keyref"))
            # ET.SubElement(xref, "text")
            # dita_file_tree = ET.parse(defined_path)
            dita_file_tree = ET.parse(defined_path)
            dita_file_root = dita_file_tree.getroot()
            for keydef in dita_file_root.iter("keydef"):
                if keydef.get("keys").strip() == apiname.get("keyref").strip():
                    href_text = "".join(keydef.itertext()).strip()
            print("----------------------apiname text--------------------")
            print(href_text.strip())
            print("----------------------apiname text--------------------")
            apiname.text = href_text.strip()
            print(apiname.text)

    for pt in root.iter("ph"):
        # print(xref.get("keyref"))
        # For each xref, perform the following operations:
        # 1. Get the ditamap file per platform
        # 2. Extract href text from ditamap
        # 3. Set href text in current dita
        href_text = ""
        if pt.get("keyref") is not None:
            # xref.text = str(xref.get("keyref"))
            # ET.SubElement(xref, "text")
            # dita_file_tree = ET.parse(defined_path)
            dita_file_tree = ET.parse(defined_path)
            dita_file_root = dita_file_tree.getroot()
            for keydef in dita_file_root.iter("keydef"):
                if keydef.get("keys").strip() == pt.get("keyref").strip():
                    href_text = "".join(keydef.itertext()).strip()
            print("----------------------pt text--------------------")
            print(href_text.strip())
            print("----------------------pt text--------------------")
            pt.text = href_text.strip()
            print(pt.text)

    # Android

    # Rust

    # Get href from keydef in ditamap files
    #     <keydef keys="onClientRoleChanged" href="../API/onClientRoleChanged.dita">
    #         <topicmeta>
    #             <keywords>
    #                 <keyword>onClientRoleChanged</keyword>
    #             </keywords>
    #         </topicmeta>
    #     </keydef>
    #
    # <xref keyref="setChannelProfile"/> for each API category

    # xref with keyref
    for xref in root.iter("xref"):
        # print(xref.get("keyref"))
        # For each xref, perform the following operations:
        # 1. Get the ditamap file per platform
        # 2. Extract href text from ditamap
        # 3. Set href text in current dita
        href_text = ""
        if xref.get("keyref") is not None:
            # xref.text = str(xref.get("keyref"))
            # ET.SubElement(xref, "text")
            # dita_file_tree = ET.parse(defined_path)
            dita_file_tree = ET.parse(defined_path)
            dita_file_root = dita_file_tree.getroot()
            for keydef in dita_file_root.iter("keydef"):
                if keydef.get("keys") == xref.get("keyref"):
                    href_text = keydef.get("href")
            print("----------------------href text--------------------")
            print(href_text)
            print("----------------------href text--------------------")

            if sys.platform == 'darwin':
                print("macOS")
                if href_text is not None and href_text != "" and not href_text.startswith("http"):
                    dir = path.join(working_dir, href_text).replace("../", "")
                elif href_text.startswith("http"):
                    xref.text = href_text
                    dir = None
                    print(xref.text)
                else:
                    dir = None
            elif sys.platform == 'win32':
                print("Windows")
                if href_text is not None and href_text != "" and not href_text.startswith("http"):
                    dir = path.join(working_dir, href_text).replace("../", "").replace("/", "\\")
                elif href_text is not None and href_text.startswith("http"):
                    xref.text = href_text
                    dir = None
                    print(xref.text)
                else:
                    dir = None
            if dir is not None:
                print(dir)
                dita_file_tree = ET.parse(dir)
                dita_file_root = dita_file_tree.getroot()
                # Get title
                title = dita_file_root.find("./title")
                title_ph = dita_file_root.find("./title/ph")
                print(title)
                if title.text is not None:
                    title_text = title.text
                elif title_ph.get("keyref") is not None:
                    # dita_file_tree = ET.parse(defined_path)
                    dita_file_tree = ET.parse(defined_path)
                    dita_file_root = dita_file_tree.getroot()
                    for keydef in dita_file_root.iter("keydef"):
                        if keydef.get("keys").strip() == title_ph.get("keyref").strip():
                            title_text = "".join(keydef.itertext()).strip()

                print("----------------------title text--------------------")
                print(title_text)
                print("----------------------title text--------------------")
                xref.text = title_text
                print(xref.text)


        # xref with href
        # Example:
        # <plentry id="0">
        #    <pt><ph keyref="REMOTE_VIDEO_STATE_STOPPED"/></pt>
        #    <pd>0: 远端视频默认初始状态。在 <xref href="enum_remotevideostatereason.dita#enum_remotevideostatereason/3"/>、 <xref href="enum_remotevideostatereason.dita#enum_remotevideostatereason/5"/> 或
        #    <xref href="enum_remotevideostatereason.dita#enum_remotevideostatereason/7"/> 的情况下，会报告该状态。</pd>
        # </plentry>
        elif xref.get("href") is not None and not xref.get("href").startswith("http") and not xref.get("href").endswith(
                "md") and not xref.get("href").startswith("mailto"):
            href = xref.get("href")
            splitted = href.split("#")
            if len(splitted) >= 2:
                dita_file_tree = ET.parse(path.join(working_dir, "API", splitted[0]))
                print(splitted[0])
                dita_file_root = dita_file_tree.getroot()
                plentry_id_list = splitted[1].split("/")
                plentry_id = plentry_id_list[-1]
                print("------------WWWWWWWWWWWWWWWWWWWWWWWWWWWWW------------")
                print(plentry_id)
                print("------------WWWWWWWWWWWWWWWWWWWWWWWWWWWWW------------")
                # Get the element by path
                for plentry in dita_file_root.findall("./refbody/section/parml/plentry"):
                    if plentry.get("id") == plentry_id:
                        ph_tag = plentry.find("./pt/ph")
                        ph_tag_key = ph_tag.get("keyref")
                        print("------------WWWWWWWWWWWWWW  PH Tag KEY  WWWWWWWWWWWWWWW------------")
                        print(ph_tag_key)
                        print("------------WWWWWWWWWWWWWWWWW PH Tag KEY     WWWWWWWWWWWW------------")

                        dita_file_tree = ET.parse(defined_path)
                        dita_file_root = dita_file_tree.getroot()
                        for keydef in dita_file_root.iter("keydef"):
                            if keydef.get("keys") == ph_tag_key:
                                for text in keydef.itertext():
                                    if text is not None:
                                        print(type(text))
                                        # new_text = text.text
                                        # print(new_text)
                                        # if new_text is not None:
                                        href_text = href_text + text

                xref.text = href_text
                # xref.text = href_text
                # print(xref.text)

            else:
                # 请确保在调用其他 API 前先调用
                #                     <xref keyref="createAgoraRtcEngine1" />
                #                     和
                #                     <apiname keyref="create2" />
                #                     创建并初始化
                #                     <xref href="class_irtcengine.dita" />
                #                     。
                print("-------- Doom Wheel --------------")
                print(path.join(working_dir, "API", href))
                print("-------------Doom Wheel------------")
                dita_file_tree = ET.parse(path.join(working_dir, "API", href))
                dita_file_root = dita_file_tree.getroot()

                title = dita_file_root.find("./title/ph")
                if title.text is not None:
                    title_text = title.text
                elif title.get("keyref") is not None:
                    # dita_file_tree = ET.parse(defined_path)
                    dita_file_tree = ET.parse(defined_path)
                    dita_file_root = dita_file_tree.getroot()
                    for keydef in dita_file_root.iter("keydef"):
                        if keydef.get("keys").strip() == title.get("keyref").strip():
                            title_text = "".join(keydef.itertext()).strip()
                xref.text = title_text


        elif xref.get("href") is not None and xref.get("href").startswith("http"):
            xref.text = xref.text + " (" + xref.get("href") + ")"

            # Ref to a file
            # elif len(splitted) == 1:
            # dita_file_tree = ET.parse(path.join(working_dir, "API", splitted[0]))
            # dita_file_root = dita_file_tree.getroot()

    # Android

    # Rust

    # Get the following information
    # API ID (reference id = "xxx")
    # Short description (shortdesc)
    # Detailed description ()
    # Parameter description
    # Return value

    # Get API ID
    api_id = root.attrib
    api_id = api_id.get("id")
    print("----------------------- App ID ------------------------")
    print(api_id)
    print("----------------------- App ID ------------------------")

    # Get API name
    api_name = ""
    api_name_tag = root.find("title")
    for q in api_name_tag.itertext():
        api_name = api_name + q
    print("----------------------- App Name ------------------------")
    print(api_name)
    print("----------------------- App Name ------------------------")

    # Get short description
    short_desc_text = ""
    short_desc = root.find('shortdesc')
    if short_desc is not None:
        for text in short_desc.itertext():
            short_desc_text = short_desc_text + text

    if short_desc is None:
        # short_desc = "Empty"
        short_desc_text = ""
    print("----------------------- Short desc ------------------------")
    print(short_desc_text)
    print("----------------------- Short desc ------------------------")

    # Get detailed description
    # Tables exist in pd and detailed desc. Need to process tables.
    detailed_desc = ""
    for section in root.findall('./refbody/section'):
        # print(section)
        if section.get("id") == "detailed_desc":
            title = section.find("./title")
            if title is not None:
                title.clear()

            for text in section.itertext():
                if text is not None:
                    print(type(text))
                    # new_text = text.text
                    # print(new_text)
                    # if new_text is not None:
                    detailed_desc = detailed_desc + text

    detailed_desc = detailed_desc.strip(" \n ")
    # detailed_desc_text = ""

    # for i in detailed_desc:
    # detailed_desc_text = detailed_desc_text + i

    print("----------------------- Detailed desc ------------------------")
    print(detailed_desc)
    print("----------------------- Detailed desc ------------------------")

    api_desc = short_desc_text + detailed_desc

    # Get parameter description <plentry> by id
    # parameter name <pt>
    # parameter description <pd>
    # Use a dictionary for param/desc pair
    param_pair = {}
    param_name = ""
    param_desc = ""
    # Tables exist in pd and detailed desc. Need to process tables.
    for param_list in root.findall('./refbody/section/parml'):
        # print(section)
        # For each <plentry> in <parml>, get <pt> and <pd>
        # if param_list.get("id") != "return_values":
        for child in param_list:
            if child.find("pt") is not None:
                param_name = child.find("pt").text
                if param_name is None and child.find("./pt/ph") is not None:
                    param_name = child.find("./pt/ph").text
                else:
                    print("Something unexpected happened for " + child.text)
                print(child.find("./pd").text)
                for text in child.find("./pd").itertext():
                    if text is not None:
                        print(text)
                        param_desc = param_desc + text

            param_pair[param_name] = param_desc
            # Clean the param_desc variable to get new values
            param_desc = ""

    print(param_pair)

    json_array = []
    for key, value in param_pair.items():
        # Append a new dictionary separating keys and values from the original dictionary to the array:
        json_array.append({key: value})
    print(json_array)

    # Get return value
    # No need to tell each return value
    # Get return value
    return_values = ""
    for section in root.findall('./refbody/section'):
        print(section)
        if section.get("id") == "return_values":
            title = section.find("./title")
            if title is not None:
                title.clear()
            for text in section.itertext():
                print(text)
                return_values = return_values + text

    print("----------------------- Return values ------------------------")
    print(return_values)
    print("----------------------- Return values ------------------------")

    # ------------------------------------------------------------------
    # Migrate the information to a JSON file.
    # ------------------------------------------------------------------
    # See the following template
    # {
    #   "id": "",
    #   "description": "",
    #   "parameters": [
    #     {"param1": "desc"},
    #     {"param2": "desc"}
    #   ],
    #   "returns": ""
    # }

    data = {}

    data['id'] = api_id
    data['name'] = api_name
    data['description'] = api_desc
    data['parameters'] = json_array
    data['returns'] = return_values.strip("\n ")

    print(data)

    file_name = path.basename(path.normpath(file_dir))
    name_list = file_name.split(".")
    json_name = name_list[0]


    # Write to JSON
    # Test only: ensure_ascii=False is only used for UTF-8 characters
    with open(path.join(path.dirname(__file__), "json_files", json_name + '.json'), 'w', encoding="utf-8") as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)

    # Call the function to create a single JSON file
    # create_json_from_xml(working_dir, file_dir)


# Clean the json_files folder
for root, dirs, files in os.walk(path.join(path.dirname(__file__), "json_files")):
    for file in files:
        os.remove(os.path.join(root, file))

for file_name in os.listdir(path.join(working_dir, 'API')):
    if file_name.endswith(
            ".dita") and file_name != "API-overview.dita" and file_name != "api_data_type.dita" and file_name in rust_topicref_list:
        create_json_from_xml(working_dir, path.join(working_dir, 'API', file_name), android_full_path, cpp_full_path,
                             rust_full_path)

# Join all files in the json_files folder
# List of json files to merge
files = list()
for json_name in os.listdir(path.join(path.join(path.dirname(__file__), "json_files"))):
    files.append(path.join(path.dirname(__file__), "json_files", json_name))

print(files)


def merge_JsonFiles(files):
    result = list()
    for file in files:
        print(file)
        with open(file, 'r', encoding="utf-8") as infile:
            result.append(json.load(infile))

    with open(json_file, 'w', encoding="utf-8") as output_file:
        json.dump(result, output_file, ensure_ascii=False, indent=4)


# Merge the individual JSON files to a single JSON file
merge_JsonFiles(files)