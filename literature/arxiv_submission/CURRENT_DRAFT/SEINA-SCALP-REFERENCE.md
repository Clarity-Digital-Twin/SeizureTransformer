PhysioNet
Share
About
Explore 

Search PhysioNet
Log in
 Database  Open Access

Siena Scalp EEG Database
Paolo Detti 

Published: Aug. 11, 2020. Version: 1.0.0

When using this resource, please cite: (show more options)
Detti, P. (2020). Siena Scalp EEG Database (version 1.0.0). PhysioNet. RRID:SCR_007345. https://doi.org/10.13026/5d4a-j060

Additionally, please cite the original publication:
Detti, P., Vatti, G., Zabalo Manrique de Lara, G. EEG Synchronization Analysis for Seizure Prediction: A Study on Data of Noninvasive Recordings. Processes 2020, 8(7), 846; https://doi.org/10.3390/pr8070846

Please include the standard citation for PhysioNet: (show more options)
Goldberger, A., Amaral, L., Glass, L., Hausdorff, J., Ivanov, P. C., Mark, R., ... & Stanley, H. E. (2000). PhysioBank, PhysioToolkit, and PhysioNet: Components of a new research resource for complex physiologic signals. Circulation [Online]. 101 (23), pp. e215–e220. RRID:SCR_007345.

Abstract
The database consists of EEG recordings of 14 patients acquired at the Unit of Neurology and Neurophysiology of the University of Siena.  Subjects include 9 males (ages 25-71) and 5 females (ages 20-58). Subjects were monitored with a Video-EEG with a sampling rate of 512 Hz, with electrodes arranged on the basis of the international 10-20 System. Most of the recordings also contain 1 or 2 EKG signals. The diagnosis of epilepsy and the classification of seizures according to the criteria of the International League Against Epilepsy were performed by an expert clinician after a careful review of the clinical and electrophysiological data of each patient.

Background
Epilepsy is interpreted as a neurological disorder characterized by the occurrences of seizures, due to abnormal excessive or synchronous neuronal activity in the brain [1]. Very importantly, the main features of epilepsy, epileptic seizures, are associated with a number of negative consequences at both short- and long-term, including the risk of falls and injuries, eventually death, psychiatric disturbances, cognitive deficits and difficulties in achieving academic, social and employment goals. Treatment options for epilepsy are  pharmacological and surgical.

However, antiepileptic drugs have limitations [2] and fail to control seizures in roughly 30% of patients, while surgery is not always an option.  In this context, an important issue is the possibility of predicting/detecting the occurrences of epileptic seizures (i.e., detecting a preictal or pre-seizure state), in order to take actions to neutralize an incoming seizure or limit the injuries (e.g., by warning alarms, applying short-acting drugs, activating stimulating devices).

The data has been collected by the Unit of Neurology and Neurophysiology at University of Siena, Italy, during a regional research project, called PANACEE [3], aiming at the development of noninvasive patient-specific monitoring/control low-cost devices for the prediction of epileptic seizures.

Methods
The database consists of EEG recordings of 14 patients monitored with a Video-EEG with a sampling rate of 512 Hz, with electrodes arranged on the basis of the international 10-20 System. All the recordings contain 1 or 2 EKG signals, too. The data were acquired employing EB Neuro and Natus Quantum LTM amplifiers, and reusable silver/gold cup electrodes. Patients were asked to stay in the bed as much as possible, either asleep or awake.

The Ethical Committee of the University of Siena approved the data in accordance with the Declaration of Helsinki. At the time of admission at the clinics, each patient signed a written informed consent in which agrees to the video registration and to the use of the data for a possible scientific divulgation.

Data Description
The database consists of 14 folders containing EEG recordings in EDF format (European Data Format). Each folder refers to a specific subject including between 1 and 5 data files with a maximum size of 2.11 GB each, and a text file containing information on data and seizures. The edf files contain signals recorded on the same or different days and the seizure events are chronologically ordered. All dates in the .edf files are de-identified.

The file subject_info.csv contains, for each subject, the gender and age, the seizure classification according to the criteria of the International League Against Epilepsy, the number of EEG channels, the number of seizures and the total recording time in minutes. IAS is focal onset impaired awareness; WIAS is focal onset without impaired awareness; FBTC is focal to bilateral tonic-clonic; T is temporal; R is right; L is left. In total, the database contains 47 seizures on about 128 recording hours.

Usage Notes
Each folder contains from 1 to 5 edf data files containing EEG and EKG recordings of a specific subject. Each folder also includes a text file named Seizures-list-PNxx.txt containing: data sampling rate (in Hz);  the list of the channels from which the EEG and EKG signals are extracted (all other channels in the edf files must be ignored); start and end time of recording, start and end time of each seizure, in the format hours.minutes.seconds. 

Noninvasive EEG data may be useful for exploring the possibility of developing a noninvasive monitoring/control devices for the prediction of seizures. The data have been presented in Detti et al [4] and employed for validating seizure prediction algorithms in [4,5,6].

Conflicts of Interest
The authors have no conflicts of interest to declare.

References
Epilepsy Foundations, Last accessed on July 17th, 2020. https://www.epilepsy.com/
CLP Deckers et al. (2003). Current limitations of antiepileptic drug therapy: a conference review. Epilepsy research, 53(1-2):1–17.
PANACEE project, Last accessed on July 17th, 2020. https://panacee. diism.unisi.it/
Detti, P., Vatti, G., & Zabalo Manrique de Lara, G. (2020). EEG synchronization analysis for seizure prediction: a study on data of non-invasive recordings. Processes, 8(7), doi.org/10.3390/pr8070846.
Detti, P., Lara, G. Z., Bruni, R., Pranzo, M., Sarnari, F., & Vatti, G. (2018). A Patient-specific Approach for Short-term Epileptic Seizures Prediction through the Analysis of EEG synchronization. IEEE Transactions on Biomedical Engineering, 1-1. doi:10.1109/tbme.2018.2874716.
Billeci, L, Marino, D, Insana, L, Vatti, G, & Varanini, M. (2018). Patient-specific seizure prediction based on heart rate variability and recurrence quantification analysis. PLoS One. 13(9). doi: 10.1371/journal.pone.0204339. eCollection 2018.
Share
    
Access
Access Policy:
Anyone can access the files, as long as they conform to the terms of the specified license.

License (for files):
Creative Commons Attribution 4.0 International Public License

Discovery
DOI (version 1.0.0):
https://doi.org/10.13026/5d4a-j060

DOI (latest version):
https://doi.org/10.13026/s309-a395

Corresponding Author
You must be logged in to view the contact information.
Files
Total uncompressed size: 20.3 GB.

Access the files
Download the ZIP file (13.0 GB)
Download the files using your terminal: wget -r -N -c -np https://physionet.org/files/siena-scalp-eeg/1.0.0/
Download the files using AWS command line tools: aws s3 sync --no-sign-request s3://physionet-open/siena-scalp-eeg/1.0.0/ DESTINATION
 Visualize waveforms

Folder Navigation: <base>
Name	Size	Modified
PN00		
PN01		
PN03		
PN05		
PN06		
PN07		
PN09		
PN10		
PN11		
PN12		
PN13		
PN14		
PN16		
PN17		
LICENSE.txt(download)	14.5 KB	2020-08-01
RECORDS(download)	667 B	2020-07-17
SHA256SUMS.txt(download)	4.8 KB	2020-08-11
subject_info.csv(download)	563 B	2020-08-05

PhysioNet
MIT Laboratory for Computational Physiology

National Institute of Biomedical Imaging and Bioengineering (NIBIB) under NIH grant number R01EB030362

Navigation
Discover Data
Share Data
About
News
Explore
Data
Software
Tutorials
Challenges
