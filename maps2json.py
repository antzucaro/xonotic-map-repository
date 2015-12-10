#!/usr/bin/env python3
# Description: Loops through a directory of map pk3s and outputs JSON with map information
# Author: Tyler "-z-" Mulligan

import zipfile, os, re, hashlib, json, subprocess, shutil, collections, time
from datetime import datetime
from datetime import timedelta

import multiprocessing
from queue import Queue
import time
            
def main():

    start_time = time.monotonic()

    global path_packages, path_mapshots, extract_mapshots, parse_entities
    global packs_maps, packs_entities_fail, packs_corrupt, packs_other
    global entities_dict, entities_list
    global errors
    global q
 
    path_packages = './resources/packages/'
    path_mapshots = './resources/mapshots/'

    extract_mapshots = True
    parse_entities = True

    errors = False
    packs_entities_fail = []
    packs_corrupt = []
    packs_other  = []

    packs_maps = []

    entities_dict = {

        # health / armor
        'item_armor_small': 'item_armor_small',
        'item_armor1': 'item_armor_small',
        'item_armor_shard': 'item_armor_small',
        'item_armor_medium': 'item_armor_medium',
        'item_armor_large': 'item_armor_large',
        'item_armor25': 'item_armor_large',
        'item_armor2': 'item_armor_large',
        'item_armor_body': 'item_armor_large',
        'item_armor_big': 'item_armor_big',
        'item_armor_combat': 'item_armor_big',
        'item_armor_mega': 'item_armor_big',
        'item_health_small': 'item_health_small',
        'item_health1': 'item_health_small',
        'item_health_medium': 'item_health_medium',
        'item_health25': 'item_health_medium',
        'item_health_large': 'item_health_large',
        'item_health_mega': 'item_health_mega',
        'item_health100': 'item_health_mega',

        # powerups
        'item_strength': 'item_strength',
        'item_quad': 'item_strength',
        'item_invincible': 'item_invincible',
        'item_enviro': 'item_invincible',

        # flags
        'item_flag_team1': 'item_flag_team1',
        'team_CTF_redflag': 'item_flag_team1',
        'item_flag_team2': 'item_flag_team2',
        'team_CTF_blueflag': 'item_flag_team2',
        'item_flag_team3': 'item_flag_team3',
        'item_flag_team4': 'item_flag_team4',
        'item_flag_neutral': 'item_flag_neutral',

        # ammo
        'item_bullets': 'item_bullets',
        'item_spikes': 'item_bullets',
        'ammo_bullets': 'item_bullets',
        'item_rockets': 'item_rockets',
        'ammo_rockets': 'item_rockets',
        'ammo_grenades': 'item_rockets',
        'ammo_nails': 'item_rockets',
        'ammo_cells': 'item_rockets',
        'item_cells': 'item_cells',
        'ammo_lightning': 'item_cells',
        'ammo_slugs': 'item_cells',
        'ammo_bfg': 'item_cells',
        'item_shells': 'item_shells',
        'ammo_shells': 'item_shells',
        'item_plasma': 'item_plasma',
        'item_minst_cells': 'item_minst_cells',

        # weapons
        'weapon_shotgun': 'weapon_shotgun',
        'weapon_electro': 'weapon_electro',
        'weapon_nailgun': 'weapon_electro',
        'weapon_lightning': 'weapon_electro',
        'weapon_hagar': 'weapon_hagar',
        'weapon_supernailgun': 'weapon_hagar',
        'weapon_plasmagun': 'weapon_hagar',
        'weapon_vortex': 'weapon_vortex',
        'weapon_railgun': 'weapon_vortex',
        'weapon_nex': 'weapon_vortex',
        'weapon_crylink': 'weapon_crylink',
        'weapon_bfg': 'weapon_crylink',
        'weapon_vaporizer': 'weapon_vaporizer',
        'weapon_minstanex': 'weapon_vaporizer',
        'weapon_rifle': 'weapon_rifle',
        'weapon_campingrfile': 'weapon_rifle',
        'weapon_sniperrifle': 'weapon_rifle',
        'weapon_blaster': 'weapon_blaster',
        'weapon_laser': 'weapon_blaster',
        'weapon_devastator': 'weapon_devastator',
        'weapon_rocketlauncher': 'weapon_devastator',
        'weapon_grenadelauncher': 'weapon_grenadelauncher',
        'weapon_mortar': 'weapon_grenadelauncher',
        'weapon_machinegun': 'weapon_machinegun',
        'weapon_uzi': 'weapon_machinegun',
        'weapon_supershotgun': 'weapon_machinegun',
        'weapon_fireball': 'weapon_fireball',
        'weapon_shockwave': 'weapon_shockwave',
        'weapon_seeker': 'weapon_seeker',
        'weapon_arc': 'weapon_arc',
        'weapon_minelayer': 'weapon_minelayer',
        'weapon_hook': 'weapon_hook',

        # player spawns
        'info_player_deathmatch': 'info_player_deathmatch',
        'info_player_team1': 'info_player_team1',
        'team_CTF_redplayer': 'info_player_team1',
        'team_CTF_redspawn': 'info_player_team1',
        'info_player_team2': 'info_player_team2',
        'team_CTF_blueplayer': 'info_player_team2',
        'team_CTF_bluespawn': 'info_player_team2',
        'info_player_team3': 'info_player_team3',
        'info_player_team4': 'info_player_team4',
        'info_player_start': 'info_player_start',
        #'info_player_survivor': 'info_player_survivor',
        #'info_player_race': 'info_player_race',
        #'info_player_attacker': 'info_player_attacker',
        #'info_player_defender': 'info_player_defender'

    }

    entities_list = entities_dict.keys()

    # Create the queue and process pool
    q = multiprocessing.JoinableQueue()
    jobs = []
    for i in range(multiprocessing.cpu_count()):
        p = multiprocessing.Process(target=worker)
        jobs.append(p)
        p.start()                 

    # Process all the files
    for file in sorted(os.listdir(path_packages)):
        if file.endswith('.pk3'):
            q.put(file)
    
    q.join()

    for j in jobs:
        q.put(None)

    q.join()

    for j in jobs:
        j.join()


    # Write error.log
    if errors:
        dt = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        fo = open('error.log', 'a')

        if len(packs_other) != 0:
            e_no_map = 'One or more archives did not contain a map'
            print('\n' + e_no_map)

            fo.write('\n' + dt + ' - ' + e_no_map + ':\n')
            fo.write('\n'.join(packs_other) + '\n')

        if len(packs_corrupt) != 0:
            e_corrupt = 'One or more archives were corrupt'
            print('\n' + e_corrupt)

            fo.write('\n' + dt + ' - ' + e_corrupt + ':\n')
            fo.write('\n'.join(packs_corrupt) + '\n')

        if len(packs_entities_fail) != 0:
            e_no_map = 'One or more entities files failed to parse'
            print('\n' + e_no_map)

            fo.write('\n' + dt + ' - ' + e_no_map + ':\n')
            fo.write('\n'.join(packs_entities_fail) + '\n')

        fo.close()

    output = {}
    output['data'] = packs_maps

    # for debugging
    #print(json.dumps(output, sort_keys=True, indent=4, separators=(',', ': ')))

    fo = open('./resources/data/maps.json', 'w')
    fo.write(json.dumps(output))
    fo.close()

    end_time = time.monotonic()
    print(timedelta(seconds=end_time - start_time))


# The worker thread pulls an item from the queue and processes it
def worker():
    for item in iter( q.get, None):
        process_pk3(item)
        q.task_done()
    q.task_done()


def process_pk3(file):

    print('Processing ' + file)

    data = {}
    data['pk3'] = file
    data['shasum'] = hash_file(path_packages + file)
    data['filesize'] = os.path.getsize(path_packages + file)
    data['date'] = os.path.getmtime(path_packages + file)
    data['bsp'] = {}
    data['mapshot'] = []
    data['mapinfo'] = []
    data['waypoints'] = []
    data['map'] = []
    data['radar'] = []
    data['title'] = False
    data['description'] = False
    data['gametypes'] = []
    data['author'] = False
    data['license'] = False

    # temp variables
    bsps = []
    bspnames = {}

    try:
        zip = zipfile.ZipFile(path_packages + file)
        filelist = zip.namelist()

        # Get the bsp name(s)
        for member in filelist:
            if re.search('^maps/.*bsp$', member):
                bsp_info = zip.getinfo(member)
                bspnames[member] = member.replace('maps/','').replace('.bsp','')
                # this is coming back as a float
                epoch = int(datetime(*bsp_info.date_time).timestamp())
                data['date'] = epoch
                bsps.append(member)
                data['bsp'][bspnames[member]] = {}

        # One or more bsps has been found (it's a map package)
        if len(bsps):

            # If this option is on, attempt to extract enitity info
            if parse_entities:

                for bsp in bsps:
                    
                    bspname = bspnames[bsp]
#                    t_bspname = threading.current_thread().name + "_" + bspname
                    t_bspname = multiprocessing.current_process().name + "_" + bspname

                    zip.extract(bsp, './resources/bsp/' + t_bspname)
                                                       
                    bsp_entities_file = './resources/entities/' + t_bspname + '.ent'

                    with open(bsp_entities_file, 'w') as f:
                        subprocess.call(["./bsp2ent", './resources/bsp/' + t_bspname + "/" + bsp], stdin=subprocess.PIPE, stdout=f)

                    data['bsp'][bspname] = parse_entities_file(data['bsp'][bspname], data['pk3'], bsp_entities_file)

                    shutil.rmtree('./resources/bsp/' + t_bspname)

            # Find out which of the important files exist in the package
            for member in filelist:
                for bsp in data['bsp']:

                    rbsp = re.escape(bsp)

                    if re.search('^maps/' + rbsp + '\.(jpg|tga|png)$', member):
                        data['mapshot'].append(member)
                        if extract_mapshots:
                            zip.extract(member, path_mapshots)

                    if re.search('^maps/' + rbsp + '\.mapinfo$', member):
                        mapinfofile = member
                        data['mapinfo'].append(member)

                    if re.search('^maps/' + rbsp + '\.waypoints$', member):
                        data['waypoints'].append(member)

                    if re.search('^maps/' + rbsp + '\.map$', member):
                        data['map'].append(member)

                    if re.search('^gfx/' + rbsp + '_(radar|mini)\.(jpg|tga|png)$', member):
                        data['radar'].append(member)

                    if re.search('^maps/' + rbsp + '\.ent', member):

                        if parse_entities:

                            zip.extract(member, './resources/entities/' + t_bspname)
                                                       
                            entities_file = './resources/entities/' + t_bspname + '/' + member
                            entities_from_ent = parse_entities_file(data['bsp'][bspname], data['pk3'], entities_file)
                            data['bsp'][bspname].update(entities_from_ent)
                            shutil.rmtree('./resources/entities/' + t_bspname)

                if re.search('^maps/(LICENSE|COPYING|gpl.txt)$', member):
                    data['license'] = True

            # If the mapinfo file exists, try and parse it
            if len(data['mapinfo']):
                mapinfo = zip.open(mapinfofile)
                
                for line in mapinfo:
                    line = line.decode('unicode_escape').rstrip()

                    if re.search('^title.*$', line):
                        data['title'] = line.partition(' ')[2]

                    elif re.search('^author.*', line):
                        data['author'] = line.partition(' ')[2]

                    elif re.search('^description.*', line):
                        data['description'] = line.partition(' ')[2]

                    elif re.search('^(type|gametype).*', line):
                        data['gametypes'].append(line.partition(' ')[2].partition(' ')[0])

            packs_maps.append(data)
        else:
            errors = True
            packs_other.append(file)
    
    except zipfile.BadZipfile:
        errors = True
        print('Corrupt file: ' + file)
        packs_corrupt.append(file)
        pass


def hash_file(filename):
   """"This function returns the SHA-1 hash
   of the file passed into it"""

   # make a hash object
   h = hashlib.sha1()

   # open file for reading in binary mode
   with open(filename,'rb') as file:

       # loop till the end of the file
       chunk = 0
       while chunk != b'':
           # read only 1024 bytes at a time
           chunk = file.read(1024)
           h.update(chunk)

   # return the hex representation of digest
   return h.hexdigest()


def parse_entities_file(bsp, pk3, entities_file):

    try:
        f = open(entities_file)
        for line in iter(f):
            for entity in entities_list:
                real_entity = entities_dict[entity]
                if re.search(entity, line):
                    if 'entities' not in bsp:
                        bsp['entities'] = {}
                    if real_entity not in bsp['entities']:
                        bsp['entities'][real_entity] = 1
                    else:
                        bsp['entities'][real_entity] += 1

        if 'entities' in bsp:
            all_bsp_entities = bsp['entities']
            if len(all_bsp_entities):
                sorted_entities = collections.OrderedDict(sorted(all_bsp_entities.items()))
                bsp['entities'] = sorted_entities

        f.close()
        os.remove(entities_file)

    except UnicodeDecodeError:
        errors = True
        bsp['entities'] = {}
        packs_entities_fail.append(entities_file)
        print("Failed to parse entities file for: " + pk3)

    return bsp

if __name__ == "__main__":
    main()
