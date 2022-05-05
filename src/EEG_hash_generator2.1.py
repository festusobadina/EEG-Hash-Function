# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#         EEG HASH GENERATOR 2.1            #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#           Author           |   Student ID #
# ------------------------------------------#
# Adewale Temiloluwa Obadina |    ao19206   #
# -------------------------------------------#

# Description
# -----------
#   The purpose of this program is to take a text file of EEG brain recordings and return a hash of the data within.
#   This is to support the idea that EEG can possibly be used as a method of biometric authentication.

#   Change Log
#   + Rate distortion method (needs to be cleaned)
#   + response for not inputting which sha to use
#   ¬ Need to finish rate distortion and add graph showing function


import os, hashlib, time

# ===================================#
#              VARIABLES            #
# ===================================#


# ---String variables to store the concatenated binary data for each channel for hashing.
raw_string = ""
rounded_string = ""

# ---Hash variables that get updated with each call of the compression funciton.
#   set_sha() will decide which version to use
raw_sha = ""
rounded_sha = ""

# ---The level at which raw data is quantized (rounded).
quantization_value = 1

# ---Tent map variables
tent_map_x = 0.419
tent_map_r = 1.71328107957338452

# ---Initial vector for compression function
initial_vector = 1085813135847353183

# ---Empty, pre-defined dictionary for EEG data.
#       [0] = Raw data (float).
#       [1] = Binary conversion of raw data (32 bits).
#       [2] = quantized data (int).
#       [3] = Binary conversion of quantized data (8 bits).
#       [4] = Rate Distortion (Squared-error)
eeg_data_dict = {
    'FP1':   [[], [], [], []],
    'FP2':   [[], [], [], []],
    'F7':    [[], [], [], []],
    'F8':    [[], [], [], []],
    'AF1':   [[], [], [], []],
    'AF2':   [[], [], [], []],
    'FZ':    [[], [], [], []],
    'F4':    [[], [], [], []],
    'F3':    [[], [], [], []],
    'FC6':   [[], [], [], []],
    'FC5':   [[], [], [], []],
    'FC2':   [[], [], [], []],
    'FC1':   [[], [], [], []],
    'T8':    [[], [], [], []],
    'T7':    [[], [], [], []],
    'CZ':    [[], [], [], []],
    'C3':    [[], [], [], []],
    'C4':    [[], [], [], []],
    'CP5':   [[], [], [], []],
    'CP6':   [[], [], [], []],
    'CP1':   [[], [], [], []],
    'CP2':   [[], [], [], []],
    'P3':    [[], [], [], []],
    'P4':    [[], [], [], []],
    'PZ':    [[], [], [], []],
    'P8':    [[], [], [], []],
    'P7':    [[], [], [], []],
    'PO2':   [[], [], [], []],
    'PO1':   [[], [], [], []],
    'O2':    [[], [], [], []],
    'O1':    [[], [], [], []],
    'X':     [[], [], [], []],
    'AF7':   [[], [], [], []],
    'AF8':   [[], [], [], []],
    'F5':    [[], [], [], []],
    'F6':    [[], [], [], []],
    'FT7':   [[], [], [], []],
    'FT8':   [[], [], [], []],
    'FPZ':   [[], [], [], []],
    'FC4':   [[], [], [], []],
    'FC3':   [[], [], [], []],
    'C6':    [[], [], [], []],
    'C5':    [[], [], [], []],
    'F2':    [[], [], [], []],
    'F1':    [[], [], [], []],
    'TP8':   [[], [], [], []],
    'TP7':   [[], [], [], []],
    'AFZ':   [[], [], [], []],
    'CP3':   [[], [], [], []],
    'CP4':   [[], [], [], []],
    'P5':    [[], [], [], []],
    'P6':    [[], [], [], []],
    'C1':    [[], [], [], []],
    'C2':    [[], [], [], []],
    'PO7':   [[], [], [], []],
    'PO8':   [[], [], [], []],
    'FCZ':   [[], [], [], []],
    'POZ':   [[], [], [], []],
    'OZ':    [[], [], [], []],
    'P2':    [[], [], [], []],
    'P1':    [[], [], [], []],
    'CPZ':   [[], [], [], []],
    'nd':    [[], [], [], []],
    'Y':     [[], [], [], []]
}


# ===================================#
#              FUNCTIONS             #
# ===================================#


# ---Set variables depending on whether SHA2 or SHA3 is being used
#   Default to SHA3
def set_sha(version="3"):
    global raw_sha
    global rounded_sha

    if version == "2":
        #   Secure Hash Algorithm 2
        raw_sha = hashlib.sha256()
        rounded_sha = hashlib.sha256()

    elif version == "3":
        #   Secure Hash Algorithm 3
        raw_sha = hashlib.sha3_256()
        rounded_sha = hashlib.sha3_256()
    else:
        print("Invalid input. Defaulting to SHA3")
        print("------------------------------------------------------------------")
        raw_sha = hashlib.sha3_256()
        rounded_sha = hashlib.sha3_256()


# ---File operations.
def open_file():
    #   Save the current working directory into , allows file to be opened without specifying full filepath.
    #   Remove newline tag from each line and split the rounded_string into tokens.
    #   Skipping lines where last value is not a number (first few "file description" lines).
    #   NOTE if running on linux, swap "\\" with "//" on line 117.
    __file_path__ = os.path.realpath(os.path.join(
        os.getcwd(), os.path.dirname(__file__)))

    while True:
        try:
            file = input("Enter filename to hash:\t\t\t\t")
            filename = __file_path__ + "\\test data\\" + file
            file = open(filename, "r")
            break
        except Exception:
            print("File does not exist, please re-enter\n")

    for line in file:

        words = (line.strip()).split(' ')

        if (words[-2]).isnumeric() == False:
            continue
        else:
            #   Append EEG data to corresponding channel in  EEG dictionary.
            for key in eeg_data_dict:
                if key == words[-3]:
                    #   Split data lines from "header" lines.
                    if words[-2] != "chan":
                        eeg_data_dict[key][0].append(float(words[-1]))
    file.close()


# ---Two's complement to represent negative EEG values.
#   function adapted from source https://www.tutorialspoint.com/How-to-do-twos-complement-on-a-16-bit-signal-using-Python.
def twos_complement(number):
    #   TC = number XOR with 65535 (16 binary 1's) and + 1.
    temp = (number ^ 65535) + 1
    return (bin(temp))


# ---For converting rounded data into binary
#   Quantized binary is of a fixed length of 8 bits, with first bit reserved for sign bit
def rounded_data_to_bin(data):
    #   If data is greater than 0, strip binary prefix
    if (data > 0):
        return (bin(data).lstrip("0b")).zfill(8)

    #   If data is less than 0, only strip negative sign
    elif (data < 0):
        temp = str(data).lstrip("-")

        return "1" + (bin(int(temp)).lstrip("0b")).zfill(7)

    #   If data is equal to 0, return 0
    else:
        #   NOTE -- Will accept 7 0's but breaks on the eight?
        return "0000000"
        # return "00000000"


# ---Data quantization.
#   Data is quantized (rounded) to "n" to  reduce number of bits needed to represent values.
#   In order to reduce computational load (possibly important in corpora of GB sizes).
def quantization(data):
    global quantization_value

    rounded = round(float(data) / quantization_value) * quantization_value

    return (rounded)


# ---Convert raw and quantized data into binary.
#   For each list of raw and quantized data in each channel, convert into binary and store in respective list (see line 10).
def convert_to_binary(channel_name):
    eeg_data_list = eeg_data_dict[channel_name]

    for item in eeg_data_list[0]:

        whole, decimal = str(item).split(".")

        # ---Processing raw data.
        #    If string is negative, split string into whole and decimal.
        #    Take twos compliment of negative number and append bin of decimal to it.
        #    NOTE that when decimal is converted, takes number as whole integer, not decimal.
        #    e.g. -8.921 -> -8 -> 1111111111111000
        #                -> 0.921 -> 921 -> 1110011001

        if whole.startswith("-"):
            eeg_data_dict[channel_name][1].append(
                (twos_complement(int(whole)).lstrip("-0b").zfill(16)) + bin(int(decimal)).lstrip("0b").zfill(16))

        elif whole.startswith("0") == False:
            #   If number is positive, split into whole and dec, convert individually and append.
            eeg_data_dict[channel_name][1].append(
                bin(int(whole)).lstrip("0b").zfill(16) + bin(int(decimal)).lstrip("0b").zfill(16))

        #   If number is 0, just append decimal conversion.
        else:
            eeg_data_dict[channel_name][1].append(
                "0" + bin(int(decimal)).lstrip("0b").zfill(31))

        # ---Processing rounded data.
        result = whole + "." + decimal

        quantized_result = quantization(result)

        eeg_data_dict[channel_name][2].append(quantized_result)
        eeg_data_dict[channel_name][3].append(rounded_data_to_bin(quantized_result))


# ---Split the string containing all of the binary data into a list.
#   Each element will be a chunk of the binary string of "n" bits.
#   Currently blocks of 1024 bits.
def string_to_list(eeg_string):
    start = 0
    end = 1023

    eeg_list = []

    for x in eeg_string:
        eeg_list.append(eeg_string[start:end])

        #   Split the next block.
        start += 1024
        end += 1024

        #   Stop when there are no more bits left.
        if start > len(eeg_string):
            break

    return eeg_list


# ---Funciton to strip the "0." prefix from tent map output.
#   Will make the decimal of the float and convert that into an int (e.g. 0.123[float] -> 123[int]).
#   Easier to operate on whole numbers as opposed to decimals.
def remove_decimal(decimal_value):
    decimal_value = str(decimal_value)
    decimal_value = int(decimal_value.removeprefix("0."))
    return decimal_value


# ---Generate a tent map (see https://en.wikipedia.org/wiki/Tent_map)
#   Chaotic vairiables help to increase complexity of program.
#   Chaos in hashing may sound counter-intuative, but as long as "x" and "r" key values are the same, the output is reproducable.
#   "x" and "r" key values can be kept constant and public,
#   or changed randomly with each instance of hash verification required (as long as they can be properly shared between client and authenticator), to make collision attacks even harder.
def generate_tent_map(x, r, size):
    tent_output = []

    #   Tent map function.
    for i in range(size):
        if (x < 0.5):
            x = r * x

        elif (x > 0.5):
            x = r * (1 - x)

        temp = bin(remove_decimal(x)).lstrip("0b")
        tent_output.append(temp)

    return tent_output


# ---Perform binary XOR to obfuscate sensitive data with chaotic output.
def xor_bits(tent_map_value, binary_value):
    # convert tent map value to binary and remove "0b" prefix.
    output = int(tent_map_value, 2) ^ int(binary_value, 2)

    return bin(output).lstrip("0b")


# ---Permute the hash for additional layer of complexity.
def permutation(rounded_string):
    rounded_string = rounded_string.lstrip("0b")

    s1 = rounded_string[:255]
    s2 = rounded_string[256:512]
    s3 = rounded_string[513:768]
    s4 = rounded_string[769:]

    s1, s3 = s3, s1
    s2, s4 = s4, s2
    s2, s3 = s3, s2
    string_list = [s1, s2, s3, s4]
    print(s1)
    print(s2)
    print(s3)
    print(s4)

    return ("".join(string_list))


# ---Compress the result of XOR of the tent map and EEG data into a 64 byte string.
def compression(list: list, flag):
    # Initial Vector can be changed at discretion,
    # another pseudo-key to with tent map "x" and "r" to make reproduction without this information difficult.

    #global initial_vector

    block = 0
    tent_output = generate_tent_map(0.246, 1.619, len(list))
    hash = ''

    while block <= (len(list) - 1):

        if block == 0:

            hash = bin(initial_vector ^ int(list[block], 2))
            block += 1

            temp = permutation(hash).encode('utf-8')

            if flag == "raw":
                raw_sha.update(temp)
            elif flag == "round":
                rounded_sha.update(temp)

        else:

            hash = bin(int(list[block], 2) ^ int(temp, 2))

            hash = bin(int(tent_output[block], 2) ^ int(hash, 2))

            temp = permutation(hash).encode('utf-8')
            if flag == "raw":
                raw_sha.update(temp)
            elif flag == "round":
                rounded_sha.update(temp)

            block += 1

    return hash


# ---XOR each 1024 bit blocks with the corresponding tent map result.
def xor_list(tent_output, eeg_bin_list):
    block = 0
    result = []

    while block < len(eeg_bin_list):
        x = xor_bits(tent_output[block], eeg_bin_list[block])
        result.append(x)
        block += 1

    return result


# ===================================#
#           MAIN PROGRAM            #
# ===================================#


if __name__ == "__main__":

    # print("------------------------------------------")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("~    EEG Hash Generator 2.1 by Adewale Obadina   ~")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

    sha_version = input("Would you like to hash with SHA2 or SHA3?:\t")
    print("------------------------------------------------------------------")

    # If sha_version input is omitted, default to Version 3
    set_sha(sha_version)

    open_file()

    # Start timer
    start_time = time.time()

    for channel in eeg_data_dict:
        convert_to_binary(channel)

    for key in eeg_data_dict:

        for number in eeg_data_dict[key][1]:
            raw_string += str(number)

        for number in eeg_data_dict[key][3]:
            rounded_string += str(number)

    raw_eeg_bin_list = string_to_list(raw_string)
    rounded_eeg_bin_list = string_to_list(rounded_string)

    raw_tent_output = generate_tent_map(
        tent_map_x, tent_map_r, len(raw_eeg_bin_list))
    rounded_tent_output = generate_tent_map(
        tent_map_x, tent_map_r, len(rounded_eeg_bin_list))

    raw_hashed_block = xor_list(raw_tent_output, raw_eeg_bin_list)
    rounded_hashed_block = xor_list(rounded_tent_output, rounded_eeg_bin_list)

    compression(raw_hashed_block, "raw")
    compression(rounded_hashed_block, "round")

    # Stop timerFround
    stop_time = time.time()

    print("\n\n----------------------------------------------------------------------------------")
    print("Raw Hash:\t|", raw_sha.hexdigest().upper())
    print("----------------------------------------------------------------------------------")
    print("Quantized Hash: |", rounded_sha.hexdigest().upper())
    print("----------------------------------------------------------------------------------")
    print("Hashing process took", stop_time - start_time, "seconds to complete.")

    print(len(raw_string))
    print(len(rounded_string))


    #DICTIONARY TEST COMMENTS
    #---------------------------
    # test_channel = "nd"
    # print(type(eeg_data_dict[test_channel][0][0]))
    # print("Raw data\n", eeg_data_dict[test_channel][0], "\n")
    
    # print(type(eeg_data_dict[test_channel][1][0]))
    # print("Binary of raw data\n", eeg_data_dict[test_channel][1], "\n")
    
    # print(type(eeg_data_dict[test_channel][2][0]))
    # print("quantized data\n", eeg_data_dict[test_channel][2], "\n")
    
    # print(type(eeg_data_dict[test_channel][3][0]))
    # print("Binary of quantized data\n", eeg_data_dict[test_channel][3], "\n")
    # ---------------------------
