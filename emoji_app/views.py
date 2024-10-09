from django.shortcuts import render
from django.conf import settings
import emoji
import numpy as np

def encrypt(request):
    text = ""  # Initialize the variable
    emoji=""
    display="none"
    if request.method == 'POST':
        # Handle form submission
        text = request.POST.get('text', '')  # Get the value of the 'text' field from the form
        key = request.POST.get('key', '') 
        # Replace this with your actual encryption logic
        encrypted_text =  encryption(text,key)
        print("C.T",encrypted_text)
        # Set the 'gajanand' variable to be displayed in the template
        emoji = encrypt_to_emoji(encrypted_text)
        # emoji = encrypted_text
        if(emoji != ""):
            display="block"

    # Pass the 'gajanand' variable to the template
    return render(request, 'emoji_encryption.html', {'Text': text, 'emoji':emoji, 'display':display} )


def decrypt(request):
    decrypted_text = ""  # Initialize the variable
    emoji_input=""
    display="none"
    
    if request.method == 'POST':
        # Handle form submission
        emoji_input=""
        emoji_input = request.POST.get('emoji', '')  # Get the value of the 'text' field from the form
        keys = request.POST.get('key', '')
        # Replace this with your actual encryption logic
        texts = decrypt_to_text(emoji_input) 
        decrypted_text = decryption(texts,keys)
        # print("dt",decrypted_text)
        

        if(decrypted_text != ""):
            display="block"
        
    return render(request, 'emoji_decryption.html', { 'text':decrypted_text,'emoji': emoji_input, 'display': display})


def encrypt_to_emoji(input_text):
    pt_to_emoji=''
    for char in input_text:
        pt_to_emoji += emoji.emojize(cldr_short_names[ord(char)])
        # print(cldr_short_names[ord(char)])
        print(ord(char))
    return pt_to_emoji

def decrypt_to_text(input_text):
    print("Input Text:", input_text)
    input_text = emoji.demojize(input_text)
    print("Demojized Text:", input_text)
    input_list = [f":{item}:" for item in input_text.split(":") if item]
    print("Input List:", input_list)
    ot = ""
    for emoj in input_list:
        try:
            index = cldr_short_names.index(emoj)
            ot += chr(index)
            print(index)
        except ValueError:
            ot += chr(32)  # If emoji not found, append a space
    print("Output Text:", ot)
    return ot
  
def KSA(key):
    key_length = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + int(key[i % key_length])) % 256
        S[i], S[j] = S[j], S[i]
    return S

def PRGA(S, n):
    i = 0
    j = 0
    key = []
    while n > 0:
        n -= 1
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        key.append(K)
    return key

def encryption(plaintext, key):
    S = KSA(key)
    keystream = np.array(PRGA(S, len(plaintext)))
    plaintext = np.array([ord(i) for i in plaintext])
    cipher = keystream ^ plaintext
    ctext = ''.join([chr(c) for c in cipher])
    return ctext

def decryption(ciphertext, key):
    S = KSA(key)
    keystream = np.array(PRGA(S, len(ciphertext)))
    ciphertext = np.array([ord(i) for i in ciphertext])
    decoded = keystream ^ ciphertext
    dtext = ''.join([chr(c) for c in decoded])
    return dtext


char_list='''ABCDEFGHIJKLMNOPQRSTUVWXYZ
abcdefghijklmnopqrstuvwxyz
0123456789
`~!@#$%^&*()_+-=[]{}|\\:;'<>,./ '''





cldr_short_names = [
':grinning_face_with_big_eyes:',
':grinning_face_with_smiling_eyes:',
':beaming_face_with_smiling_eyes:',
':grinning_squinting_face:',
':grinning_face_with_sweat:',
':rolling_on_the_floor_laughing:',
':face_with_tears_of_joy:',
':slightly_smiling_face:',
':upside-down_face:',
':winking_face:',
':smiling_face_with_smiling_eyes:',
':smiling_face_with_halo:',
':smiling_face_with_heart-eyes:',
':star-struck:',
':face_blowing_a_kiss:',
':kissing_face:',
':kissing_face_with_closed_eyes:',
':kissing_face_with_smiling_eyes:',
':smiling_face_with_tear:',
':face_with_tongue:',
':winking_face_with_tongue:',
':zany_face:',
':squinting_face_with_tongue:',
':money-mouth_face:',
':face_with_hand_over_mouth:',
':shushing_face:',
':thinking_face:',
':zipper-mouth_face:',
':face_with_raised_eyebrow:',
':neutral_face:',
':expressionless_face:',
':face_without_mouth:',
':smirking_face:',
':unamused_face:',
':face_with_rolling_eyes:',
':grimacing_face:',
':face_exhaling:',
':lying_face:',
':relieved_face:',
':pensive_face:',
':sleepy_face:',
':drooling_face:',
':sleeping_face:',
':face_with_medical_mask:',
':face_with_thermometer:',
':face_with_head-bandage:',
':nauseated_face:',
':face_vomiting:',
':sneezing_face:',
':hot_face:',
':cold_face:',
':woozy_face:',
':exploding_head:',
':cowboy_hat_face:',
':partying_face:',
':disguised_face:',
':smiling_face_with_sunglasses:',
':nerd_face:',
':face_with_monocle:',
':confused_face:',
':worried_face:',
':slightly_frowning_face:',
':frowning_face:',
':face_with_open_mouth:',
':hushed_face:',
':astonished_face:',
':flushed_face:',
':pleading_face:',
':frowning_face_with_open_mouth:',
':anguished_face:',
':fearful_face:',
':anxious_face_with_sweat:',
':sad_but_relieved_face:',
':crying_face:',
':loudly_crying_face:',
':face_screaming_in_fear:',
':confounded_face:',
':persevering_face:',
':disappointed_face:',
':downcast_face_with_sweat:',
':weary_face:',
':tired_face:',
':yawning_face:',
':face_with_steam_from_nose:',
':angry_face:',
':face_with_symbols_on_mouth:',
':smiling_face_with_horns:',
':angry_face_with_horns:',
':skull:',
':pile_of_poo:',
':clown_face:',
':ogre:',
':goblin:',
':ghost:',
':alien:',
':alien_monster:',
':robot:',
':grinning_cat:',
':grinning_cat_with_smiling_eyes:',
':cat_with_tears_of_joy:',
':smiling_cat_with_heart-eyes:',
':cat_with_wry_smile:',
':kissing_cat:',
':weary_cat:',
':crying_cat:',
':pouting_cat:',
':see-no-evil_monkey:',
':hear-no-evil_monkey:',
':speak-no-evil_monkey:',
':kiss_mark:',
':love_letter:',
':heart_with_arrow:',
':heart_with_ribbon:',
':sparkling_heart:',
':growing_heart:',
':beating_heart:',
':revolving_hearts:',
':two_hearts:',
':heart_decoration:',
':heart_exclamation:',
':broken_heart:',
':heart_on_fire:',
':mending_heart:',
':red_heart:',
':orange_heart:',
':yellow_heart:',
':green_heart:',
':blue_heart:',
':purple_heart:',
':brown_heart:',
':black_heart:',
':white_heart:',
':hundred_points:',
':anger_symbol:',
':collision:',
':dizzy:',
':sweat_droplets:',
':dashing_away:',
':hole:',
':bomb:',
':speech_balloon:',
':eye_in_speech_bubble:',
':left_speech_bubble:',
':right_anger_bubble:',
':thought_balloon:',
':zzz:',
':waving_hand:',
':raised_back_of_hand:',
':hand_with_fingers_splayed:',
':raised_hand:',
':vulcan_salute:',
':OK_hand:',
':pinched_fingers:',
':pinching_hand:',
':victory_hand:',
':crossed_fingers:',
':love-you_gesture:',
':sign_of_the_horns:',
':call_me_hand:',
':backhand_index_pointing_left:',
':backhand_index_pointing_right:',
':backhand_index_pointing_up:',
':middle_finger:',
':backhand_index_pointing_down:',
':index_pointing_up:',
':thumbs_up:',
':thumbs_down:',':raised_fist:',
':oncoming_fist:',
':left-facing_fist:',
':right-facing_fist:',
':clapping_hands:',
':raising_hands:',
':open_hands:',
':palms_up_together:',
':handshake:',
':folded_hands:',
':nail_polish:',
':selfie:',
':flexed_biceps:',
':mechanical_arm:',
':mechanical_leg:',
':leg:',
':foot:',
':ear:',
':ear_with_hearing_aid:',
':nose:',
':brain:',
':anatomical_heart:',
':lungs:',
':tooth:',
':bone:',
':eyes:',
':eye:',
':tongue:',
':mouth:',
':baby:',
':child:',
':boy:',
':girl:',
':person:',
':man:',
':woman:',
':older_person:',
':old_man:',
':old_woman:',
':person_frowning:',
':man_frowning:',
':woman_frowning:',
':person_pouting:',
':man_pouting:',
':woman_pouting:',
':person_gesturing_NO:',
':man_gesturing_NO:',
':woman_gesturing_NO:',
':person_gesturing_OK:',
':person_tipping_hand:',
':person_raising_hand:',
':deaf_person:',
':person_shrugging:',
':person_bowing:',
':person_facepalming:',
':man_gesturing_OK:',
':woman_gesturing_OK:',
':man_tipping_hand:',
':woman_tipping_hand:',
':man_raising_hand:',
':woman_raising_hand:',
':deaf_man:',
':deaf_woman:',
':man_bowing:',
':woman_bowing:',
':man_facepalming:',
':woman_facepalming:',
':man_shrugging:',
':woman_shrugging:',
':health_worker:',
':man_health_worker:',
':woman_health_worker:',
':student:',
':man_student:',
':woman_student:',
':teacher:',
':man_teacher:',
':woman_teacher:',
':judge:',
':man_judge:',
':woman_judge:',
':farmer:',
':man_farmer:',
':woman_farmer:',
':cook:',
':man_cook:',
':woman_cook:',
':mechanic:',
':man_mechanic:',
':woman_mechanic:',
':factory_worker:',
':man_factory_worker:',
':woman_factory_worker:',
':office_worker:',
':man_office_worker:',
':woman_office_worker:',
':scientist:',
':man_scientist:',
':woman_scientist:',
':technologist:',
':man_technologist:',
':woman_technologist:',
':singer:',
':man_singer:',
':woman_singer:',
':artist:',
':man_artist:',
':woman_artist:',
':pilot:',
':man_pilot:',
':woman_pilot:',
':astronaut:',
':man_astronaut:',
':woman_astronaut:',
':firefighter:',
':man_firefighter:',
':woman_firefighter:',
':police_officer:',
':man_police_officer:',
':woman_police_officer:',
':man_detective:',
':person_with_white_cane:',
':man_with_white_cane:',
':woman_with_white_cane:',
':person_in_motorized_wheelchair:',
':man_in_motorized_wheelchair:',
':woman_in_motorized_wheelchair:',
':person_in_manual_wheelchair:',
':man_in_manual_wheelchair:',
':woman_in_manual_wheelchair:',
]



#  cldr_short_names = [
#     ":grinning_face:", ":grinning_face_with_big_eyes:", ":grinning_face_with_smiling_eyes:", ":beaming_face_with_smiling_eyes:",
#     ":grinning_squinting_face:", ":grinning_face_with_sweat:", ":rolling_on_the_floor_laughing:", ":face_with_tears_of_joy:",
#     ":slightly_smiling_face:", ":upside-down_face:", ":melting_face:", ":winking_face:", ":smiling_face_with_smiling_eyes:",
#     ":smiling_face_with_halo:", ":smiling_face_with_hearts:", ":smiling_face_with_heart-eyes:", ":star-struck:",
#     ":face_blowing_a_kiss:", ":kissing_face:", ":smiling_face:", ":kissing_face_with_closed_eyes:", ":kissing_face_with_smiling_eyes:",
#     ":smiling_face_with_tear:", ":face_savoring_food:", ":face_with_tongue:", ":winking_face_with_tongue:", ":zany_face:",
#     ":squinting_face_with_tongue:", ":money-mouth_face:", ":smiling_face_with_open_hands:", ":face_with_hand_over_mouth:",
#     ":face_with_open_eyes_and_hand_over_mouth:", ":face_with_peeking_eye:", ":shushing_face:", ":thinking_face:", ":saluting_face:",
#     ":zipper-mouth_face:", ":face_with_raised_eyebrow:", ":neutral_face:", ":expressionless_face:", ":face_without_mouth:",
#     ":dotted_line_face:", ":face_in_clouds:", ":smirking_face:", ":unamused_face:", ":face_with_rolling_eyes:", ":grimacing_face:",
#     ":face_exhaling:", ":lying_face:", ":shaking_face:", ":head_shaking_horizontally:", ":head_shaking_vertically:", ":relieved_face:",
#     ":pensive_face:", ":sleepy_face:", ":drooling_face:", ":sleeping_face:", ":face_with_medical_mask:", ":face_with_thermometer:",
#     ":face_with_head-bandage:", ":nauseated_face:", ":face_vomiting:", ":sneezing_face:", ":hot_face:", ":cold_face:", ":woozy_face:",
#     ":face_with_crossed-out_eyes:", ":face_with_spiral_eyes:", ":exploding_head:", ":cowboy_hat_face:", ":partying_face:",
#     ":disguised_face:", ":smiling_face_with_sunglasses:", ":nerd_face:", ":face_with_monocle:", ":confused_face:", ":face_with_diagonal_mouth:",
#     ":worried_face:", ":slightly_frowning_face:", ":frowning_face:", ":face_with_open_mouth:", ":hushed_face:", ":astonished_face:",
#     ":flushed_face:", ":pleading_face:", ":face_holding_back_tears:", ":frowning_face_with_open_mouth:", ":anguished_face:",
#     ":fearful_face:", ":anxious_face_with_sweat:", ":sad_but_relieved_face:", ":crying_face:", ":loudly_crying_face:", ":face_screaming_in_fear:",
#     ":confounded_face:", ":persevering_face:", ":disappointed_face:", ":downcast_face_with_sweat:", ":weary_face:", ":tired_face:",
#     ":yawning_face:", ":face_with_steam_from_nose:", ":enraged_face:", ":angry_face:", ":face_with_symbols_on_mouth:", ":smiling_face_with_horns:",
#     ":angry_face_with_horns:", ":skull:", ":skull_and_crossbones:", ":pile_of_poo:", ":clown_face:", ":ogre:", ":goblin:", ":ghost:",
#     ":alien:", ":alien_monster:", ":robot:", ":smiling_face_with_sunglasses:", ":nerd_face:", ":face_with_monocle:", ":confused_face:",
#     ":worried_face:", ":slightly_frowning_face:", ":frowning_face:", ":smirking_face:", ":unamused_face:", ":face_with_rolling_eyes:",
#     ":grimacing_face:", ":face_exhaling:", ":lying_face:", ":shaking_face:", ":head_shaking_horizontally:", ":head_shaking_vertically:",
#     ":relieved_face:", ":pensive_face:", ":sleepy_face:", ":drooling_face:", ":sleeping_face:", ":face_with_medical_mask:",
#     ":face_with_thermometer:", ":face_with_head-bandage:", ":nauseated_face:", ":face_vomiting:", ":sneezing_face:", ":hot_face:",
#     ":cold_face:", ":woozy_face:", ":face_with_crossed-out_eyes:", ":face_with_spiral_eyes:", ":exploding_head:", ":cowboy_hat_face:",
#     ":partying_face:", ":disguised_face:", ":smiling_face_with_sunglasses:", ":nerd_face:", ":face_with_monocle:", ":confused_face:",
#     ":worried_face:", ":slightly_frowning_face:", ":frowning_face:", ":smirking_face:", ":unamused_face:", ":face_with_rolling_eyes:",
#     ":grimacing_face:", ":face_exhaling:", ":lying_face:", ":shaking_face:", ":head_shaking_horizontally:", ":head_shaking_vertically:",
#     ":relieved_face:", ":pensive_face:", ":sleepy_face:", ":drooling_face:", ":sleeping_face:", ":face_with_medical_mask:",
#     ":face_with_thermometer:", ":face_with_head-bandage:", ":nauseated_face:", ":face_vomiting:", ":sneezing_face:", ":hot_face:",
#     ":cold_face:", ":woozy_face:", ":face_with_crossed-out_eyes:", ":face_with_spiral_eyes:", ":exploding_head:", ":cowboy_hat_face:",
#     ":partying_face:", ":disguised_face:", ":smiling_face_with_sunglasses:", ":nerd_face:", ":face_with_monocle:", ":confused_face:",
#     ":worried_face:", ":slightly_frowning_face:", ":frowning_face:", ":smirking_face:", ":unamused_face:", ":face_with_rolling_eyes:",
#     ":grimacing_face:", ":face_exhaling:", ":lying_face:", ":shaking_face:", ":head_shaking_horizontally:", ":head_shaking_vertically:",
#     ":relieved_face:", ":pensive_face:", ":sleepy_face:", ":drooling_face:", ":sleeping_face:", ":face_with_medical_mask:",
#     ":face_with_thermometer:", ":face_with_head-bandage:", ":nauseated_face:", ":face_vomiting:", ":sneezing_face:", ":hot_face:",
#     ":cold_face:", ":woozy_face:", ":face_with_crossed-out_eyes:", ":face_with_spiral_eyes:", ":exploding_head:", ":cowboy_hat_face:",
#     ":partying_face:", ":disguised_face:", ":smiling_face_with_sunglasses:", ":nerd_face:", ":face_with_monocle:", ":confused_face:",
#     ":worried_face:", ":slightly_frowning_face:", ":frowning_face:", ":smirking_face:", ":unamused_face:", ":face_with_rolling_eyes:",
#     ":grimacing_face:", ":face_exhaling:", ":lying_face:", ":shaking_face:", ":head_shaking_horizontally:", ":head_shaking_vertically:",
#     ":relieved_face:", ":pensive_face:", ":sleepy_face:", ":drooling_face:", ":sleeping_face:", ":face_with_medical_mask:",
#     ":face_with_thermometer:", ":face_with_head-bandage:", ":nauseated_face:", ":face_vomiting:", ":sneezing_face:", ":hot_face:",
#     ":cold_face:", ":woozy_face:", ":face_with_crossed-out_eyes:", ":face_with_spiral_eyes:", ":exploding_head:", ":cowboy_hat_face:",
#     ":partying_face:", ":disguised_face:", ":smiling_face_with_sunglasses:", ":nerd_face:", ":face_with_monocle:", ":confused_face:",
#     ":worried_face:", ":slightly_frowning_face:", ":frowning_face:", ":smirking_face:", ":unamused_face:", ":face_with_rolling_eyes:",
#     ":grimacing_face:", ":face_exhaling:", ":lying_face:", ":shaking_face:", ":head_shaking_horizontally:", ":head_shaking_vertically:",
#     ":relieved_face:", ":pensive_face:", ":sleepy_face:", ":drooling_face:", ":sleeping_face:", ":face_with_medical_mask:",
#     ":face_with_thermometer:", ":face_with_head-bandage:", ":nauseated_face:", ":face_vomiting:", ":sneezing_face:", ":hot_face:",
#     ":cold_face:", ":woozy_face:", ":face_with_crossed-out_eyes:", ":face_with_spiral_eyes:", ":exploding_head:", ":cowboy_hat_face:",
#     ":partying_face:", ":disguised_face:", ":smiling_face_with_sunglasses:", ":nerd_face:", ":face_with_monocle:", ":confused_face:",
#     ":worried_face:", ":slightly_frowning_face:", ":frowning_face:", ":smirking_face:", ":unamused_face:", ":face_with_rolling_eyes:",
#     ":grimacing_face:", ":face_exhaling:", ":lying_face:", ":shaking_face:", ":head_shaking_horizontally:", ":head_shaking_vertically:",
#     ":relieved_face:", ":pensive_face:", ":sleepy_face:", ":drooling_face:", ":sleeping_face:", ":face_with_medical_mask:",
#     ":face_with_thermometer:", ":face_with_head-bandage:", ":nauseated_face:", ":face_vomiting:", ":sneezing_face:", ":hot_face:",
#     ":cold_face:", ":woozy_face:", ":face_with_crossed-out_eyes:", ":face_with_spiral_eyes:", ":exploding_head:", ":cowboy_hat_face:",
#     ":partying_face:", ":disguised_face:", ":smiling_face_with_sunglasses:", ":nerd_face:", ":face_with_monocle:", ":confused_face:",
#     ":worried_face:", ":slightly_frowning_face:", ":frowning_face:", ":smirking_face:", ":unamused_face:", ":face_with_rolling_eyes:",
#     ":grimacing_face:", ":face_exhaling:", ":lying_face:", ":shaking_face:", ":head_shaking_horizontally:", ":head_shaking_vertically:",
#     ":relieved_face:", ":pensive_face:", ":sleepy_face:", ":drooling_face:", ":sleeping_face:", ":face_with_medical_mask:",
#     ":face_with_thermometer:", ":face_with_head-bandage:", ":nauseated_face:", ":face_vomiting:", ":sneezing_face:", ":hot_face:",
#     ":cold_face:", ":woozy_face:", ":face_with_crossed-out_eyes:", ":face_with_spiral_eyes:", ":exploding_head:", ":cowboy_hat_face:",
#     ":partying_face:", ":disguised_face:", ":smiling_face_with_sunglasses:", ":nerd_face:", ":face_with_monocle:", ":confused_face:",
#     ":worried_face:", ":slightly_frowning_face:", ":frowning_face:", ":smirking_face:", ":unamused_face:", ":face_with_rolling_eyes:",
#     ":grimacing_face:", ":face_exhaling:", ":lying_face:", ":shaking_face:", ":head_shaking_horizontally:", ":head_shaking_vertically:",
#     ":relieved_face:", ":pensive_face:", ":sleepy_face:", ":drooling_face:", ":sleeping_face:", ":face_with_medical_mask:",
#     ":face_with_thermometer:", ":face_with_head-bandage:", ":nauseated_face:", ":face_vomiting:", ":sneezing_face:", ":hot_face:",
#     ":cold_face:", ":woozy_face:", ":face_with_crossed-out_eyes:", ":face_with_spiral_eyes:", ":exploding_head:", ":cowboy_hat_face:",
#     ":partying_face:", ":disguised_face:", ":smiling_face_with_sunglasses:", ":nerd_face:", ":face_with_monocle:", ":confused_face:",
#     ":worried_face:", ":slightly_frowning_face:", ":frowning_face:", ":smirking_face:", ":unamused_face:", ":face_with_rolling_eyes:",
#     ":grimacing_face:", ":face_exhaling:", ":lying_face:", ":shaking_face:", ":head_shaking_horizontally:", ":head_shaking_vertically:",
#     ":relieved_face:", ":pensive_face:", ":sleepy_face:", ":drooling_face:", ":sleeping_face:", ":face_with_medical_mask:",
#     ":face_with_thermometer:", ":face_with_head-bandage:", ":nauseated_face:", ":face_vomiting:", ":sneezing_face:", ":hot_face:",
#     ":cold_face:", ":woozy_face:", ":face_with_crossed-out_eyes:", ":face_with_spiral_eyes:", ":exploding_head:", ":cowboy_hat_face:",
#     ":partying_face:", ":disguised_face:", ":smiling_face_with_sunglasses:", ":nerd_face:", ":face_with_monocle:", ":confused_face:",
#     ":worried_face:", ":slightly_frowning_face:", ":frowning_face:", ":smirking_face:", ":unamused_face:", ":face_with_rolling_eyes:",
#     ":grimacing_face:", ":face_exhaling:", ":lying_face:", ":shaking_face:", ":head_shaking_horizontally:", ":head_shaking_vertically:",
#     ":relieved_face:", ":pensive_face:", ":sleepy_face:", ":drooling_face:", ":sleeping_face:", ":face_with_medical_mask:",
#     ":face_with_thermometer:", ":face_with_head-bandage:", ":nauseated_face:", ":face_vomiting:", ":sneezing_face:", ":hot_face:",
#     ":cold_face:", ":woozy_face:", ":face_with_crossed-out_eyes:", ":face_with_spiral_eyes:", ":exploding_head:", ":cowboy_hat_face:",
#     ":partying_face:", ":disguised_face:", ":smiling_face_with_sunglasses:", ":nerd_face:", ":face_with_monocle:", ":confused_face:",
#     ":worried_face:", ":slightly_frowning_face:", ":frowning_face:", ":smirking_face:", ":unamused_face:", ":face_with_rolling_eyes:",
#     ":grimacing_face:", ":face_exhaling:", ":lying_face:", ":shaking_face:", ":head_shaking_horizontally:", ":head_shaking_vertically:",
#     ":relieved_face:", ":pensive_face:", ":sleepy_face:", ":drooling_face:", ":sleeping_face:", ":face_with_medical_mask:",
#     ":face_with_thermometer:", ":face_with_head-bandage:", ":nauseated_face:", ":face_vomiting:", ":sneezing_face:", ":hot_face:",
#     ":cold_face:", ":woozy_face:", ":face_with_crossed-out_eyes:", ":face_with_spiral_eyes:", ":exploding_head:", ":cowboy_hat_face:",
#     ":partying_face:", ":disguised_face:", ":smiling_face_with_sunglasses:", ":nerd_face:", ":face_with_monocle:", ":confused_face:",
#     ":worried_face:", ":slightly_frowning_face:", ":frowning_face:", ":smirking_face:", ":unamused_face:", ":face_with_rolling_eyes:",
#     ":grimacing_face:", ":face_exhaling:", ":lying_face:", ":shaking_face:", ":head_shaking_horizontally:", ":head_shaking_vertically:",
#     ":relieved_face:", ":pensive_face:", ":sleepy_face:", ":drooling_face:", ":sleeping_face:", ":face_with_medical_mask:",
#     ":face_with_thermometer:", ":face_with_head-bandage:", ":nauseated_face:", ":face_vomiting:", ":sneezing_face:", ":hot_face:",
#     ":cold_face:", ":woozy_face:", ":face_with_crossed-out_eyes:", ":face_with_spiral_eyes:", ":exploding_head:", ":cowboy_hat_face:",
#     ":partying_face:", ":disguised_face:", ":smiling_face_with_sunglasses:", ":nerd_face:", ":face_with_monocle:", ":confused_face:",
#     ":worried_face:", ":slightly_frowning_face:", ":frowning_face:", ":smirking_face:", ":unamused_face:", ":face_with_rolling_eyes:",
#     ":grimacing_face:", ":face_exhaling:", ":lying_face:", ":shaking_face:", ":head_shaking_horizontally:", ":head_shaking_vertically:",
#     ":relieved_face:", ":pensive_face:", ":sleepy_face:", ":drooling_face:", ":sleeping_face:", ":face_with_medical_mask:",
#     ":face_with_thermometer:", ":face_with_head-bandage:", ":nauseated_face:", ":face_vomiting:", ":sneezing_face:", ":hot_face:",
#     ":cold_face:", ":woozy_face:", ":face_with_crossed-out_eyes:", ":face_with_spiral_eyes:", ":exploding_head:", ":cowboy_hat_face:",
#     ":partying_face:", ":disguised_face:", ":smiling_face_with_sunglasses:", ":nerd_face:", ":face_with_monocle:", ":confused_face:",
#     ":worried_face:", ":slightly_frowning_face:", ":frowning_face:", ":smirking_face:", ":unamused_face:", ":face_with_rolling_eyes:",
#     ":grimacing_face:", ":face_exhaling:", ":lying_face:", ":shaking_face:", ":head_shaking_horizontally:", ":head_shaking_vertically:",
#     ":relieved_face:", ":pensive_face:", ":sleepy_face:", ":drooling_face:", ":sleeping_face:", ":face_with_medical_mask:",
#     ":face_with_thermometer:", ":face_with_head-bandage:", ":nauseated_face:", ":face_vomiting:", ":sneezing_face:", ":hot_face:",
#     ":cold_face:", ":woozy_face:"
# ]
