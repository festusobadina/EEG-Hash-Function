# EEG-Hash-Function

This is my final year capstone project for my Computer Systems Engineering course from the University of Essex.

<!-- ABOUT THE PROJECT -->
## About The Project


The motivation for this project is:
> "To provide a method of confirming integrity of EEG data when  transmitted through a 6G wireless network, via producing a unique hash of the EEG recordings."

What this motivation means is that interest and research in Brain Computer Interface (BCI) technology has been growing in the last few years. This is because of the incredible potential benefits that it can provide.

This project is focused on the premise that Electroencephalogram (EEG) data can be used as an improved means of biometric authentication, with BCI's being the required for its realistic application. 

EEG data can be used to represent the health, mental state and thoughts of a person. If a user is able to think of a thought, that specifc thought can be represented in EEG data. Therefore that thought could be used as a "pass-thought". Like how the hash of a plaintext password is stored in a database instead of the plaintext itself, the same would be done with an EEG produced "pass-thought".

The use case would be a user thinks of a thought (say a blue bicycle). The BCI technology would collect the EEG readings produced at the time of this thought. These readings would be hashed and stored in a system database as part of their login credentials. When the user wants to login to the system, they would recreate the thought of their pass-thought (the blue bicycle). Which would reproduce the same hash, and grant them access to their account.

Diagram of algorithm:
<div align="center">
  <img src="images/Hash_diagram.jpg" width=750 />
</div>

Program Output            |  Online Conversion
:-------------------------:|:-------------------------:
![alt text](images/text_to_bin_proof1.jpg)  |  ![alt text](images/text_to_bin_proof2.jpg)



## Algorithm Methodology

<ol>
    <li><a>Convert input data into binary equivalent.</a></li>
    <li><a>Divide input stream  into "blocks" of 128 bits nad store into a list.</a></li>
    <li><a>Generate a list of chaotic tent map values the same length as the number of elements in the binary array.</a></li>
    <li><a>XOR each _n_ th element of the binary array said _n_ th element from tent map and store in a new list.</a></li>
    <li><a>To compress list into one hash, XOR the first element of the list with a defined initial vector and then permute the result.</a></li>
    <li><a>Move onto the next element of the list and XOR with the result of the previous operation, then permute the output.</a></li>
    <li><a>Repeat step 6 until the list has been completely iterated through.</a></li>
    <li><a>Convert the final output into a hexadecimal equivalent.</a></li>
</ol>

## How To Use Program

1.  Download the source code aswell as the folder containing sample EEG data
2.  Ensure the EEG data folder is in the same directory that the program is to run from
3.  Run the program and enter which version of SHA to use in the logic when prompted
4.  Enter the name of the EEG file to be hashed when prompted (without filepath, including file extension)
5.  The program will output a 256 bit hash of the file provided as an input
