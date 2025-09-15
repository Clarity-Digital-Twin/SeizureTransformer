## **Machine-Learning-Based Diagnostics** **of EEG Pathology**

Keywords: _Machine Learning, Electroencephalography, Diagnostics, Pathology,_
_Features, Riemannian geometry, Convolutional Neural Networks_


Lukas A. W. Gemein [1a,b,c], Robin T. Schirrmeister [a,b], Patryk Chrabaszcz _�_ [a,b], Daniel Wilson [a], Joschka
Boedecker [c], Andreas Schulze-Bonhage [d], Frank Hutter [b], and Tonio Ball [a, d]


a _Neuromedical AI Lab, Department of Neurosurgery, Medical Center – University of Freiburg, Faculty of Medicine,_
_University of Freiburg, Engelbergerstr. 21, 79106 Freiburg, Germany_
b _Machine Learning Lab, Computer Science Department – University of Freiburg, Faculty of Engineering,_
_University of Freiburg, Georges-K¨ohler-Allee 74, 79110 Freiburg, Germany_
c _Neurorobotics Lab, Computer Science Department – University of Freiburg, Faculty of Engineering, University of_
_Freiburg, Georges-K¨ohler-Allee 80, 79110 Freiburg, Germany_
d _Freiburg Epilepsy Center, Department of Neurosurgery, Medical Center – University of Freiburg, Faculty of_
_Medicine, University of Freiburg, Breisacher Str. 64, 79106 Freiburg, Germany_


February 13, 2020


1 Corresponding author: lukas.gemein@uniklinik-freiburg.de
_Submitted preprint_ _December 17, 2019_


### **Abstract**

Machine learning (ML) methods have the potential to automate clinical EEG analysis. They can be categorized into feature-based (with handcrafted features), and end-to-end approaches (with learned features).
Previous studies on EEG pathology decoding have typically analyzed a limited number of features, decoders,
or both. For a I) more elaborate feature-based EEG analysis, and II) in-depth comparisons of both approaches, here we first develop a comprehensive feature-based framework, and then compare this framework
to state-of-the-art end-to-end methods. To this aim, we apply the proposed feature-based framework and
deep neural networks including an EEG-optimized temporal convolutional network (TCN) to the task of
pathological versus non-pathological EEG classification. For a robust comparison, we chose the Temple University Hospital (TUH) Abnormal EEG Corpus (v2.0.0), which contains approximately 3000 EEG recordings.
The results demonstrate that the proposed feature-based decoding framework can achieve accuracies on the
same level as state-of-the-art deep neural networks. We find accuracies across both approaches in an astonishingly narrow range from 81–86%. Moreover, visualizations and analyses indicated that both approaches
used similar aspects of the data, e.g., delta and theta band power at temporal electrode locations. We argue
that the accuracies of current binary EEG pathology decoders could saturate near 90% due to the imperfect
inter-rater agreement of the clinical labels, and that such decoders are already clinically useful, such as in
areas where clinical EEG experts are rare. We make the proposed feature-based framework available open
source and thus offer a new tool for EEG machine learning research.


_Lukas A. W. Gemein_ _1_ _INTRODUCTION_

### **1 Introduction**


There is a great interest in using machine learning (ML) methods for automatic electroencephalogram (EEG)
analysis, especially in the domain of clinical diagnostics based on the EEG. For example, ML has an important role in developing Brain-Computer Interfaces (BCIs) to support paralyzed people [Schr¨oer et al.
(2015)] or to improve neurological rehabilitation [Ramos-Murguialday et al. (2013), Tangermann et al. (2014),
Van Dokkum et al. (2015)]. It also forms a basis for detecting and predicting epileptic seizures [Subasi et al.
(2019), H¨ugle et al. (2018), Kiral-Kornek et al. (2018), Mirowski et al. (2009)] with the goal of warning
patients of upcoming seizures or to control brain stimulation for preventing or stopping seizure activity.
Furthermore, ML allows for the automation of the process of EEG-based sleep staging [Biswal et al. (2017)]
and neurological diagnostics of both specific diseases and disorders such as Alzheimer’s disease [Lehmann
et al. (2007)], depression [Cai et al. (2016), Hosseinifard et al. (2013)], traumatic brain injuries [Albert et al.
(2016)], and strokes [Giri et al. (2016)], or of general EEG pathology [Lopez de Diego (2017), Schirrmeister
et al. (2017a), Roy et al. (2019), Amin et al. (2019), Alhussein et al. (2019), Van Leeuwen et al. (2019)].
There are several facts that motivate the interest in automatic clinical EEG diagnosis. First, the evaluation of clinical EEGs is frequently a time-consuming and exhausting process. Second, it requires years of
training to assess pathological changes in clinical EEG recordings. Moreover, even for highly trained EEG
experts, diagnostic accuracy is subject to a number of limitations. It depends highly on individual training
and experience, consistency of rating over time, time constraints in different filter settings of frequently
subjectively defined frequency bands, and unclear criteria for the thresholding of potential changes, e.g., at
low amplitude in relation to the background EEG. Accordingly, inter-rater agreement in assessing EEGs is
known to be moderate [Landis and Koch (1977)], i.e., Grant et al. (2014) found a Fleiss’ Kappa of 0.44 when
neurologists classified recordings to one of seven classes including seizure, slowing, and normal activity. In
the more general task of classifying EEG recordings as pathological or normal, Houfek and Ellingson (1959)
and Rose et al. (1973) reported inter-rater agreements of 86% and 88% based on two neurologists. The development of algorithms for automated EEG diagnostics could support clinicians in screening EEGs. They
could not only reduce the workload of clinicians, but also allow for earlier detection and treatment of diseases,
which could enhance patient care. Furthermore, they could provide high-quality EEG interpretation and
classification to patients that cannot attend specialized centers.
We broadly categorize ML for EEG analysis into two approaches: feature-based and end-to-end methods.
Feature-based decoding methods have a long history of successful application in different EEG decoding tasks.
In this approach, typically handcrafted and _a priori_ selected features represent the data. For example, a
researcher could _a priori_ decide to use the spectral power in certain frequency bands as features, if they
assume that these bands are informative for the decoding task at hand. The choice of exact frequency bands
could then be handcrafted, such as in the common spatial patterns (CSP) algorithm for motor decoding

[M¨uller-Gerking et al. (1999)], or they could be determined by automatic feature selection, such as by the
recursive band estimation in the filter bank CSP (FBCSP) algorithm [Ang et al. (2008)]. This procedure
relies on the domain expertise of the researcher. If the _a priori_ feature decisions are sub-optimal, it can
diminish the quality of the resulting analysis. Conversely, owing to its explicit nature, interpretability of the
classification decisions is frequently considered an advantage of feature-based decoding.
Conversely, end-to-end decoding methods accept raw or minimally preprocessed data as inputs. To date,
end-to-end deep learning has attracted attention primarily owing to its success in other research fields, such
as computer vision [Krizhevsky et al. (2012)] and speech recognition [Hinton et al. (2012)]. However, it has
also recently gained momentum through the successful application of deep learning with artificial neural
networks to EEG analysis [Craik et al. (2019)]. By design, the networks learn features themselves and allow
for a joint optimization of the feature extraction and classification. This procedure can lead to superior


1
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _1_ _INTRODUCTION_


solutions or the discovery of unexpected informative features and does not require handcrafting, at least not
for the extraction of the features. End-to-end models have the reputation for being“black boxes”with regard
to the learned features; it is a challenge and an ongoing topic of intense research in the deep learning field to
understand what they have learned [Montavon et al. (2018), Sturm et al. (2016), Hartmann et al. (2018)].
Another common concern is that the complexity in the application of ML is only shifted from the domain
of feature engineering in traditional approaches to the domain of network engineering inasmuch as it could
be necessary to handcraft the networks according to the requirements of a given task.
In the literature, there is a lack of systematic comparisons of traditional feature-based versus end-to-end
ML analysis of EEGs, despite their importance for a wide range of applications. In particular, there are no
studies comparing the accuracy of pathology decoding from EEGs using a broad range of time, frequency, and
connectivity features with well-established end-to-end methods based on a large EEG data set for a robust
comparison. Past comparisons of deep learning results have frequently only considered other deep learning
results, or (rather) simple feature-based baselines (using thresholds, linear discriminant analysis, or linear
regression) with limited feature sets. This can lead to unfair comparisons among the methods. Moreover,
it can create the impression of superiority of one approach over another. It is actually possible that deep
learning could not yield an improvement over feature-based decoding in specific applications. Recently,
Rajkomar et al. (2018) demonstrated that logistic regression can compete with deep neural networks in
predicting medical events from electronic health records. To the best of our knowledge, there is no work
that compares different deep neural network architectures with a feature-based approach, especially using
a large set of features of several domains to decode the EEGs. However, we anticipate that large-scale
comparisons between feature-based and end-to-end methods will be critical to the advancement of ML
techniques for EEGs beyond the current state-of-the-art. Developing methods in both of these important
fields in a mutually informed manner will likely be fruitful for both advanced feature-based and novel endto-end EEG methodologies.
In this paper, we compare end-to-end decoding using deep neural networks to feature-based decoding
using a large set of features. We design a comprehensive study using the Temple University Hospital (TUH)
Abnormal EEG Corpus [Lopez de Diego (2017)] with approximately 3000 recordings of at least 15 min
duration each. This is a subset of the TUH EEG Corpus [Obeid and Picone (2016)], the largest publicly
available collection of EEG recordings to date. For feature-based pathology decoding, we use random forest
(RF) [Breiman (2001)], support vector machine (SVM) [Boser et al. (1992)], Riemannian geometry (RG),
and the auto-sklearn calssifier (ASC) [Feurer et al. (2015)] – an automated ML toolkit. For end-to-end
pathology decoding, we use three types of convolutional neural networks (ConvNets, in other publications
also CNN) [LeCun et al. (1999)] that have a history of successful application in different EEG decoding
tasks. These are the 4-layer ConvNet architecture Braindecode Deep4 ConvNet (BD-Deep4), which has been
successfully applied to motor decoding [Schirrmeister et al. (2017b)], velocity and speed decoding [Hammer
et al. (2013)], and pathology decoding [Schirrmeister et al. (2017a), Van Leeuwen et al. (2019)]. Importantly,
[we use Braindecode (BD)](https://github.com/TNTLFreiburg/braindecode) [1], a previously developed and evaluated deep learning toolbox for EEGs, “out of the
box” – without task-specific network engineering, i.e., without adaptation to the architectures. Furthermore,
we use a TCN [Bai et al. (2018)] that is optimized for EEG decoding with a neural architecture search. We
call this adaptation BD-TCN.
To the best of our knowledge, there are currently six published results for pathology decoding from EEGs,
five of which used the TUH Abnormal EEG Corpus (Table 1). However, only one publication [Lopez de
Diego (2017)] used handcrafted features and a classification through a CNN with a multi layer perceptron
(MLP). All other papers considered this initial feature-based decoding result as a baseline. Whereas Amin
et al. (2019) and Alhussein et al. (2019) have reported the highest accuracies in decoding pathology from


1 available for download at `[https://github.com/TNTLFreiburg/braindecode](https://github.com/TNTLFreiburg/braindecode)`


2
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _2_ _MATERIAL AND METHODS_


**Automated EEG Diagnosis** **Features** **Architecture** **ACC [%]**
Lopez de Diego (2017) Cepstral coeff. CNN + MLP 78.8
Schirrmeister et al. (2017a) BD-Deep4 85.4
Roy et al. (2019) ChronoNet 86.6
Amin et al. (2019)* AlexNet + SVM 87.3
Alhussein et al. (2019)* 3 x AlexNet + MLP 89.1
Van Leeuwen et al. (2019) [+] BD-Deep4 82.0


Table 1: Related works on pathology decoding using TUH Abnormal EEG Corpus. All approaches rely
on ConvNet architectures. Only chronologically oldest publication used handcrafted features. Publications
marked with * used pretrained models and additional training data. Publication marked with [+] did not use
TUH Abnormal EEG Corpus.


EEGs, we exclude them from our direct comparison. The papers mention“pretrained models”and additional
“10000 normal EEG recordings”, which would appear to be an extension of the TUH Abnormal EEG data
set without specifying more details. In ML, the effect of more data is commonly greater than the effect
of more elaborate algorithms [Halevy et al. (2009)]. A direct comparison of publications with access to a
substantially larger amount of training data would hence be unfair.
The paper is structured as follows. In Section 2, we provide an introduction to the TUH Abnormal EEG
Corpus upon which we base our study. We then discuss the feature and deep learning pipeline in detail and
explain how we proceeded in evaluating and comparing both approaches. The section closes with a discussion
of the analytical methods we used to assist in our interpretation of the results. In Section 3, we present and
discuss our results including an extensive comparison of both pipelines. We present a general discussion in
Section 4, and close with a brief outlook and conclusions in Section 5.

### **2 Material and Methods**


**2.1** **Data**


[We base our study on the TUH Abnormal EEG Corpus](https://www.isip.piconepress.com/projects/tuh_eeg/html/downloads.shtml) [2] (v2.0.0), which is currently unique owing to its
size and public availability and has enabled the task of general pathology decoding from EEGs. The corpus
includes 2993 recordings of at least 15 min duration obtained from 2329 unique patients and consists of a
development and separate final evaluation set (Table 2). It contains recordings of both male and female
patients of a wide age range (7 days to 96 years), thus including infants, children, adolescents, adults, and
senior patients. Pathologies diagnosed in the patients in the data set include (but are not limited to) epilepsy,
strokes, depression, and Alzheimer’s disease. The data set includes physician reports that provide additional
information regarding each EEG recording, such as main EEG findings, ongoing medication of the patient,
and medical history. In the description of the data set [3], the TUH reports an inter-rater agreement of 97–
100%. In the literature, the reported scores are typically considerably lower [Houfek and Ellingson (1959),
Rose et al. (1973)]. The almost perfect rating scores could be a consequence of the review process of the
findings that were performed by medical students that knew the diagnoses beforehand [Picone (2019)]. For
more information on the data set see Lopez de Diego (2017) and Obeid and Picone (2016).


2 available for download at `[https://www.isip.piconepress.com/projects/tuh_eeg/html/downloads.shtml](https://www.isip.piconepress.com/projects/tuh_eeg/html/downloads.shtml)`
3 `[https://www.isip.piconepress.com/projects/tuh_eeg/downloads/tuh_eeg_abnormal/v2.0.0/_AAREADME.txt](https://www.isip.piconepress.com/projects/tuh_eeg/downloads/tuh_eeg_abnormal/v2.0.0/_AAREADME.txt)`


3
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _2_ _MATERIAL AND METHODS_


**TUH Abnormal EEG** **Non-pathological** **Pathological** **Intersection**
**Corpus (v2.0.0)** **Recordings** **Patients** **Recordings** **Patients** **Patients**
**Development set** 1371 1237 1346 893 54
**Final evaluation set** 150 148 126 105 0

**Total** 1521 1385 1472 998 54


Table 2: Number of recordings and patients in TUH Abnormal EEG Corpus (v2.0.0). For certain patients,
there exist several recordings. For other patients in the development set, there exist normal and abnormal
recordings. There is no overlap of patients in development and the final evaluation set.


**2.2** **Common preprocessing in both feature and end-to-end pipeline**


Typically, at least minimal preprocessing of the raw EEG data is applied in both scenarios, relying on handcrafted feature extraction and based on end-to-end approaches. We applied the preprocessing steps described
below to both scenarios to normalize the input distribution and thus stabilize the deep network learning process, a common practice in deep learning applications, and to stabilize feature extraction. However, the
latter requires additional steps that are described in Section 2.4. Importantly, our general preprocessing did
not preselect any EEG features. As in our earlier work on EEG pathology decoding with deep ConvNets

[Schirrmeister et al. (2017a)], we included the following preprocessing steps: First, we selected a subset of
21 electrode positions (Figure 1) following the international 10-20 placement [Jasper (1958)] because these
electrode positions occurred in all the individual recordings in the data set. Then, we discarded the first 60 s
of every recording because we observed a large number of recording artifacts in this period, which could have
been caused by rearrangement of the electrode cap or by finding a comfortable seating position. Moreover,
we used a maximum of 20 min of every recording to avoid considerable feature generation and resampling
times for exceptionally long recordings. As in our previous work Schirrmeister et al. (2017a) and in the
work by Van Leeuwen et al. (2019), EEG recordings were downsampled to 100 Hz and clipped at _±_ 800 _µV_
to reject unphysiologically extreme values and to ensure comparability to these previous studies. Although
Roy et al. (2019) performed their experiments at 250 Hz, we chose to use 100 Hz for better comparability
with the other approaches, and to avoid motor artifacts. However, this could place us at a disadvantage in
the direct comparison with Roy et al. (2019). Our preprocessing partially uses code from Python libraries
MNE [4] and resampy [5] .


**2.3** **End-to-end decoding with deep neural networks**


**2.3.1** **Neural network architectures**


We used different neural network architectures including ConvNets and TCNs to decode the pathology from
the EEG recordings. First, we used a four-layered ConvNet architecture called BD-Deep4 as previously
introduced by Schirrmeister et al. (2017b). The BD-Deep4 architecture [Figure 2] has an initial separated
convolution (first temporal, then spatial). Subsequently, it has several blocks consisting of convolution and
max-pooling and uses exponential linear units as activation functions. It is a rather general architecture that
has proven to generalize well to several EEG decoding tasks such as motor (imagery) decoding [Schirrmeister
et al. (2017b)], velocity and speed decoding [Hammer et al. (2013)], and pathology decoding [Schirrmeister
et al. (2017a), Van Leeuwen et al. (2019)]. We applied BD-Deep4 without any further adjustments to its


4 available for download at `[https://github.com/mne-tools/mne-python](https://github.com/mne-tools/mne-python)`
5 available for download at `[https://github.com/bmcfee/resampy](https://github.com/bmcfee/resampy)`


4
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _2_ _MATERIAL AND METHODS_



![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-6-1.png)



![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-6-0.png)









Figure 1: Topographical map of 21 EEG channel subset of international 10-20 placement [Jasper (1958)]
common in all recordings included in TUH Abnormal EEG Corpus (v2.0.0).


architecture.

![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-6-24.png)

![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-6-25.png)

![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-6-26.png)

![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-6-27.png)

![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-6-28.png)


Figure 2: Four-layered BD-Deep4 as introduced by Schirrmeister et al. (2017b). Initial separated convolution
is followed by several convolution and max-pooling blocks.


Next, we used a TCN architecture [Figure 3] that was evaluated in a Master thesis by Chrabaszcz _�_
(2018). The TCN was originally proposed by Bai et al. (2018) as an alternative to recurrent neural networks
(RNN) [Rumelhart et al. (1988)]. It is the most complex and deepest architecture under investigation in the
present study. The optimization by Chrabaszcz _�_ (2018) resulted in five levels of blocks consisting of temporal
convolutions with 55 channels each as well as max-pooling. We call this optimized architecture Braindecode
TCN (BD-TCN). For more information on the optimized hyperparameters, see Table S2.
Furthermore, we used another ConvNet architecture introduced by Schirrmeister et al. (2017b) called


5
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _2_ _MATERIAL AND METHODS_





![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-7-1.png)



![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-7-3.png)






|Residual Block<br>Residual Block<br>...<br>Residual Block|Col2|Col3|
|---|---|---|
|**Residual Block**<br>**Residual Block**<br>**Residual Block**<br>**...**|**Residual Block**|**Residual Block**|
|**Residual Block**<br>**Residual Block**<br>**Residual Block**<br>**...**|**Residual Block**||
|**Residual Block**<br>**Residual Block**<br>**Residual Block**<br>**...**|||











Figure 3: General architecture of TCN as introduced by Bai et al. (2018) and search base explored in Master
thesis by Chrabaszcz _�_ (2018) to find BD-TCN.


Braindeocde Shallow ConvNet (BD-Shallow). The network [Figure 4], as in the BD-Deep4 network, has an
initial separated convolution; however, it is the only convolution in the entire architecture. The well-known
FBCSP algorithm [Ang et al. (2008)] inspired the BD-Shallow architecture, in particular the squaring and
logarithmic nonlinearities. It was designed to specifically extract the logarithm of the band power of EEG
signals. We applied BD-Shallow, as BD-Deep, without any further adjustments to its architecture.
Moreover, we used a reimplementation of another ConvNet architecture called EEGNet that was originally
introduced by Lawhern et al. (2018). We call this reimplementation Braindecode EEGNet (BD-EEGNet).
Again, the architecture has a separated initial convolution. Furthermore, the architecture is remarkable
owing to its small number of parameters (see Table S3).


6
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _2_ _MATERIAL AND METHODS_

![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-8-18.png)

![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-8-20.png)


Figure 4: BD-Shallow architecture as originally introduced by Schirrmeister et al. (2017b) inspired by FBCSP
algorithm [Ang et al. (2008)].


**2.3.2** **Training of neural networks**


We trained the networks in a cropped manner with equally-sized, maximally overlapping crops as described
by Schirrmeister et al. (2017b). The receptive field of the networks automatically determines the size of the
crops. All networks are exposed to approximately 600 signal samples at a time, except the TCN which has
a receptive field of approximately 900 samples [Table S3]. Unlike the original paper by Schirrmeister et al.
(2017a), we used optimizer AdamW [Loshchilov and Hutter (2017)] over Adam [Kingma and Ba (2014)]
to minimize the categorical cross-entropy loss function. AdamW decouples weight decay updates and the
optimization of the loss function, which allows for better generalization [Loshchilov and Hutter (2017)]. We
used cosine annealing [Loshchilov and Hutter (2016)] to schedule the learning rates for the gradient and
weight decay updates. We did not perform learning rate restarts.


**2.4** **Feature-based decoding**


**2.4.1** **Additional preprocessing prior to feature extraction**


After general preprocessing common to both pipelines (see Section 2.2), we applied several additional steps
in the feature-based pipeline. In the special case of connectivity feature extraction, we first filtered entire
signals to a selected frequency range in the time domain to avoid the creation of filtering artifacts at the
start and end points of the signal segments. We split every recording into equally sized, nonoverlapping
signal segments called crops of 600 samples, i.e., given the sampling frequency of 100 Hz, this corresponded
to 6 s, to be maximally comparable to the end-to-end pipeline, where the receptive field of the architectures
determines the crop size [S3]. We discarded crops with values of _±_ 800 _µV_ to stabilize feature generation.
This resulted in the exclusion of one recording (subject 00008184, session s00 ~~1~~ t001), as one channel was not
properly recorded, meaning each measurement at every time point exceeded the outlier value.


**2.4.2** **Feature extraction**


We computed a large set of features describing time, frequency, and connectivity structure of the EEG signals
that have all been used to characterize EEGs [Subasi (2007), Logesparan et al. (2012), Kuhlmann et al.
(2008), Kumar et al. (2010), Quiroga et al. (1997), Hjorth (1970), James and Lowe (2003), Petrosian (1995),
Inouye et al. (1991), Roberts et al. (1999), Balli and Palaniappan (2009), Peng et al. (1995), Watter (2014),
Minasyan et al. (2010), van Putten et al. (2005), Esteller et al. (2001), Katz (1988), Lachaux et al. (1999)]. We


7
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _2_ _MATERIAL AND METHODS_


generated features on every crop based on Discrete Fourier Transform (FT), Continuous and Discrete Wavelet
Transform (CWT and DWT), and between-electrode connectivity features based on the Hilbert Transform

[Table 3]. Furthermore, we parsed age and gender of the patients from the European Data Format [Kemp
et al. (1992)] recording file headers as optional additional features. The feature implementations partially
use code from the Python libraries PyEEG [6] and PyWavelets [7] . The implementations can be found in our
[feature decoding toolbox Brainfeatures](https://github.com/TNTLFreiburg/brainfeatures) [8] .

|CWT/DWT+<br>Bounded variation<br>Maximum<br>Mean<br>Minimum<br>Power<br>Power ratio<br>Spectral entropy<br>Variance|FT<br>Maximum<br>Mean<br>Minimum<br>Peak frequency<br>Power<br>Power ratio<br>Spectral entropy<br>Value range<br>Variance|Patient information<br>Age<br>Gender|
|---|---|---|
|**CWT/DWT**+<br>Bounded variation<br>Maximum<br>Mean<br>Minimum<br>Power<br>Power ratio<br>Spectral entropy<br>Variance|**FT**<br>Maximum<br>Mean<br>Minimum<br>Peak frequency<br>Power<br>Power ratio<br>Spectral entropy<br>Value range<br>Variance|**Riemannian**<br>Covariance matrix|
|**CWT/DWT**+<br>Bounded variation<br>Maximum<br>Mean<br>Minimum<br>Power<br>Power ratio<br>Spectral entropy<br>Variance|**FT**<br>Maximum<br>Mean<br>Minimum<br>Peak frequency<br>Power<br>Power ratio<br>Spectral entropy<br>Value range<br>Variance|**Connectivity**<br>Phase Locking Value|



**Time** Hjorth mobility Minimum
Detrended Fluctuation Analysis* Hurst exponent Nonlinear energy
Energy Kurtosis Petrosian fractal dimension*
Fisher information* Line length Skewness
Fractal dimension Lyauponov exponent* SVD entropy*
Higuchi fractal dimension Maximum Zero crossings
Hjorth activity Mean Zero crossings of derivative
Hjorth complexity Median


Table 3: All implemented features sorted by feature domain. Feature domains are CWT/DWT, FT, Patient
[information, RG, Connectivity, and Time. Features marked with * were computed using PyEEG. Features](https://github.com/forrestbao/pyeeg)
marked with [+] [were computed using PyWavelets.](https://github.com/PyWavelets/pywt)


For the CWT, DWT, and FT feature computation, we weighted time domain crops with a BlackmanHarris window function to enhance the spectral estimation and reduce the effect of leakage. In preliminary
experiments [Gemein (2017)], we tested different window functions. The Blackman-Harris window yielded
best results, although the choice of the window function had only minor effects on the decoding accuracy.
We extracted frequency features from bands 0–2 Hz, 2–4 Hz, 4–8 Hz, 8–13 Hz, 13–18 Hz, 18–24 Hz, 24–30
Hz, and 30–50 Hz using FT and a band overlap of 50%. We chose the bands to match the frequency bands
commonly used in the literature. Furthermore, we observed superior results in preliminary experiments when
using a band overlap [Gemein (2017)]. We chose wavelet scales for CWT and levels for DWT to match these
bands as closely as possible.
For connectivity feature computation, we transformed the frequency-filtered time-crops using the Hilbert
Transform to extract the signal phase.
The dimension of the feature vectors, including all feature values of domains CWT, DWT, FT, Connectivity, and Time, was _F_ = 8631.


6 available for download at `[https://github.com/forrestbao/pyeeg](https://github.com/forrestbao/pyeeg)`
7 available for download at `[https://github.com/PyWavelets/pywt](https://github.com/PyWavelets/pywt)`
8 available for download at `[https://github.com/TNTLFreiburg/brainfeatures](https://github.com/TNTLFreiburg/brainfeatures)`


8
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _2_ _MATERIAL AND METHODS_


**Time-resolved features** Feature generation resulted in a feature matrix _M_ _i_ _∈_ R _[C]_ _[i]_ _[×][F]_ for every recording,
where _I_ is the total number of recordings, _C_ _i_ is the number of analyzed 6-s crops _i ∈_ _I_, and _F_ is the
dimension of the feature vector. For time-resolved (non-aggregated) decoding, we considered every feature
vector of every crop as an independent example. This drastically increased the number of training examples,
which could be beneficial in the training phase. However, it also resulted in higher memory consumption
and higher learning times.


**Aggregated features** For aggregated decoding, we computed the aggregate of all time-crop feature matrices _M_ _i_ _∈_ R _[C]_ _[i]_ _[×][F]_ . Therefore, we used the median as the aggregation function, such that we obtained a
single feature vector of length _F_ for each recording. In previous experiments [Gemein (2017)], the median
proved to be the best aggregation function in terms of decoding accuracy, although, again, the choice only
had a minor effect. Aggregation drastically reduces the feature matrix size, which allows for faster learning
and prediction. However, it has the disadvantage of discarding all time-resolved information as it collapses
features of all crops of a recording into a single feature vector. The shape of the final aggregated feature
matrix was _M_ _aggregate_ _∈_ R _[I][×][F]_ .


**Dimensionality reduction** We reduced the feature dimension _F_ in preliminary experiments using principal component analysis (PCA) [Wold et al. (1987)]; however, independent of the choice of principal components or ratio of variance, the application of PCA led to a decrease in decoding accuracy.


**Covariance matrices** For Riemannian-geometry-based decoding (see below) we computed a covariance
feature matrix Σ _i_ _∈_ R _[C]_ _[i]_ _[×][E][∗][E]_ for every crop, where _E_ is the number of electrodes. Therefore, we used
the Python package pyRiemann [9] . We independently tested the Euclidean and the geometric means to
aggregate covariance matrices of the crops, such that we obtained a feature vector of length _E ∗_ ( _E_ + 1) _/_ 2
for each recording and aggregation type. The shape of the final covariance feature matrix was _M_ _riemann_ _∈_
R _[I][×][E][∗]_ [(] _[E]_ [+1)] _[/]_ [2] .


**2.4.3** **Feature-based classifiers**


After feature generation, we used the feature matrix as an input to several feature-based ML models. We used
an SVM with radial basis function (RBF) kernel, as commonly used in the literature [Lehmann et al. (2007),
Cai et al. (2016)]. Furthermore, we used an RF classifier which is, by design, robust towards overfitting
and hence a reliable baseline model. Furthermore, we also applied the automated ML toolkit ASC [10] as it
has the potential to yield superior results owing to the automatic ensemble selection and hyperparameter
optimization. For more information on this toolkit see Feurer et al. (2015). Finally, we evaluated the
Riemannian-geometry-based decoding as implemented in the Python package pyRiemann [11] using an SVM
with an RBF kernel, as it has recently achieved state-of-the art results in several BCI decoding tasks [Lotte
[et al. (2018)]. All models under investigation relied on implementations in scikit-learn](https://scikit-learn.org/stable/) [12] [Pedregosa et al.
(2011)].


9 available for download at `[https://github.com/alexandrebarachant/pyRiemann](https://github.com/alexandrebarachant/pyRiemann)`
10 available for download at `[https://github.com/automl/auto-sklearn](https://github.com/automl/auto-sklearn)`
11 see footnote 9
12 available for download at `[https://scikit-learn.org/stable/](https://scikit-learn.org/stable/)`


9
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _2_ _MATERIAL AND METHODS_


**2.5** **Evaluation of performance**


We performed 5-fold cross-validation (CV) on the development set, such that each recording in the development set was predicted exactly once. We did not shuffle data during splitting; rather, we used chronologically
ordered splits. During CV, we optimized the hyperparameters of our feature-based models [see Table S1].
For final evaluation, we evaluated our models on the held back final evaluation set. We trained models on
the full development set and predicted the examples in the final evaluation set. We repeated final evaluation
five times to manage the statistical variances caused by initialization of certain models.
We report the accuracy score as _ACC_ = [#][ of correct ] # of examples [p][redictions] for the development and final evaluation

sets as averages over the CV folds and final evaluation repetitions, respectively.
We used a statistical sign test [Dixon and Mood (1946)] to validate the predicted labels in the final
evaluation for superiority of model performance ( _H_ 1). To provide a conservative estimate, occurring ties
were equally split to both classes. We rejected the null hypothesis ( _H_ 0: There is no difference in performance)
at a p-value _<_ 0 _._ 05.


**2.6** **Analysis**


**Handcrafted features** Because we implemented a large set of features [Table 3], we were interested in
their individual importance to the decision process. RF estimates the importance of a feature by internally
computing the “purity” of a data split obtained through a feature. In principal, the purer the data split and
the earlier the feature is considered in the trees of the forest, the higher its importance. We assigned a textual
label to all computed features described in Section 2.4 and mapped them to the average feature importance
in CV using RF. We selected subsets of the features based on their textual labels with respect to frequency
band and electrode location. We then created topological plots of the average feature importance in certain
frequency ranges. Furthermore, we computed the Spearman correlation of features over the development set
and visualized the correlation map, as pronounced correlations could be a limiting factor to the interpretation
of feature-based analyses.


**Learned features** We performed input-signal perturbation to determine the informative frequency ranges
and electrode locations for identifying pathologies in the EEGs [Schirrmeister et al. (2017b)]. We computed
the network predictions of the original and randomly perturbed input signals and correlated the amplitude
change with the change of predictions. Given the labels of the examples, we could then determine whether
an increase (or decrease) of signal amplitude in a given frequency range through perturbation contributed to
more pathological (or non-pathological) predictions. Again, we made topological plots to indicate the most
correlated frequency range and electrode location with the pathological class.


**2.7** **Ensembling**


In ensembling, a number of model predictions are combined to provide an improvement over single-model
performances. Under the assumption that models make uncorrelated errors, a combination can result in the
overruling of incorrect single-model decisions. We computed the Spearman correlation of the CV predictions
of all pairs of models and visualized the resulting correlation map. Furthermore, we computed and visualized
the ratio of non-overlapping label errors of pairs of models to investigate the possibility of ensembling. Note
that ASC was excluded from this investigation because it does not provide access to internally performed CV
predictions. For ensembling, predictions are weighted. A weighting of “1” of individual model predictions is
a special case and is equivalent to majority voting. We first built an ensemble of three models based on the
highest ratio of non-overlapping label errors. We then computed an ensemble label based on the majority


10
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _3_ _RESULTS_


vote of labels computed from the individual model predictions. In addition, as an automated alternative, we
[investigated an ensemble selection technique based on auto-sklearn](https://github.com/automl/auto-sklearn) [13] introduced by Caruana et al. (2004)
that automatically selects models for ensembling and computes the optimal weights based on the validation
set. We evaluated the performance of both ensembles based on CV and final evaluation predictions of the
individual models.

### **3 Results**


**Data descriptive statistics**


We present histograms of the age distribution within the development and final evaluation sets of the TUH
Abnormal EEG Corpus (v2.0.0) in Figure 5. The age distribution, especially of the female patients, differed
between the development and final evaluation sets. Moreover, the ratio of pathological and non-pathological
examples also differed by gender and subset. The proportion of male and female patients, conversely, was
closely matched. It can be observed that recordings labeled as pathological appear more frequent with higher
age, which matches the intuition.



![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-12-2.png)





![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-12-1.png)














|100<br>90<br>80<br>70<br>60<br>50<br>40<br>30<br>20<br>10|male (4|6.7%)|Col4|Col5|Col6|Col7|Col8|Col9|fem|ale (53|.3%)|
|---|---|---|---|---|---|---|---|---|---|---|---|
|10<br>20<br>30<br>40<br>50<br>60<br>70<br>80<br>90<br>100<br>|~~me~~<br>no<br>pa|~~an age ~~<br>rmal (47<br>thologic|~~49.7 (±~~<br>.5%)<br>al (52.5|~~17.0)~~<br>%)||||~~mea~~<br>norm<br>path|~~n age 48~~<br>al (53.1<br>ological|~~.6 (± 1~~<br>%)<br>(46.9%|~~8.1)~~<br>)|


|90<br>80<br>70<br>60<br>50<br>40<br>30<br>20<br>10|ma|le (46|.4%)|Col5|Col6|Col7|Col8|Col9|Col10|Col11|fem|ale (|53.6|%)|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|10<br>20<br>30<br>40<br>50<br>60<br>70<br>80<br>90<br><br>||~~me~~<br>nor<br>pat|~~an age 4~~<br>mal (50.<br>hologica|~~8.2 (~~<br>8%)<br>l (49|~~± 16~~<br>.2%)|~~.6)~~||||~~mea~~<br>nor<br>path|~~n age 5~~<br>mal (57.<br>ologica|~~2.8 (~~<br>4%)<br>l (42.|~~± 19.~~<br>6%)|~~4)~~|













Figure 5: Development (left) and final evaluation (right) subsets of TUH Abnormal EEG Corpus (v2.0.0).
Histogram is constructed as an age pyramid subdivided into male and female patients. Different color coding
indicates pathological and non-pathological EEG recordings.


The observations are important in two respects. First, correlation of pathology with age could lead to


13 see footnote 10


11
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _3_ _RESULTS_


a situation where the trained models use patient age as a proxy for pathology. To investigate the role of
patient age in the decoding of EEG pathology further, we included age as a feature in a separate analysis
(Section 3.6). Conversely, systematic differences between the development and final evaluation sets can
reduce generalization and thus present a challenge. However, both correlation of pathology with age and
shifts between the development and final evaluation data could occur in practical application scenarios. We
hence considered these properties of the TUH data set as ecologically valid and methodologically interesting
aspects. However, they must be considered when interpreting the results achieved on this data set.


**3.1** **Aggregated feature-based decoding**


We present the aggregated feature-based decoding results in Figure 6, right half. The Riemannian-geometrybased pathological versus non-pathological EEG decoding achieved nearly 86% accuracy. Interestingly, the
decoding accuracy increased from 81% in CV to 86% in the final evaluation, which could indicate underfitting
of the training data in CV. We obtained greater than 84% accuracy using both a traditional and automated
feature-based approach.
Furthermore, we observed that all feature-based models had a higher ratio of false negatives than false
positives; that is, they rather classified pathological examples as non-pathological than the opposite (Figure 7,
bottom row). This is in consensus with results presented by Lopez de Diego (2017), Schirrmeister et al.
(2017a), and Van Leeuwen et al. (2019).







|C<br>84.69 (± 1.96) 84.73 (± 2.23) 85.76 (± 1.94) 83.3|Col2|Col3|Col4|ross-validat<br>6 (± 1.94) 83|ion<br>.10 (± 2.44) 81.59 (± 1.03) 81.26 (± 0.19) 85.19 (± 0.14)|Col7|Col8|Col9|
|---|---|---|---|---|---|---|---|---|
||||||||||
||||||||||
|~~Final evaluat~~<br>84.57 (± 0.75)<br>84.13 (± 1.07)<br>86.16 (± 1.24)<br>83.41 (± 1.04)<br>8|~~Final evaluat~~<br>84.57 (± 0.75)<br>84.13 (± 1.07)<br>86.16 (± 1.24)<br>83.41 (± 1.04)<br>8|~~Final evaluat~~<br>84.57 (± 0.75)<br>84.13 (± 1.07)<br>86.16 (± 1.24)<br>83.41 (± 1.04)<br>8|~~Final evaluat~~<br>84.57 (± 0.75)<br>84.13 (± 1.07)<br>86.16 (± 1.24)<br>83.41 (± 1.04)<br>8|~~Final evaluat~~<br>84.57 (± 0.75)<br>84.13 (± 1.07)<br>86.16 (± 1.24)<br>83.41 (± 1.04)<br>8|~~ion~~<br>.06 (± 0.57)<br>80.80 (± nan)<br>85.87 (± nan)<br>84.71 (± 0.47)|~~ion~~<br>.06 (± 0.57)<br>80.80 (± nan)<br>85.87 (± nan)<br>84.71 (± 0.47)|~~ion~~<br>.06 (± 0.57)<br>80.80 (± nan)<br>85.87 (± nan)<br>84.71 (± 0.47)|~~ion~~<br>.06 (± 0.57)<br>80.80 (± nan)<br>85.87 (± nan)<br>84.71 (± 0.47)|
||||||||||
||||||||||
||||||||||


Figure 6: Decoding accuracies of all models during CV and in final evaluation. TCN implemented in
Braindecode (BD-TCN) indicated best performance. Decoding based on RG achieved accuracy similar to
BD-TCN. BD-Deep4 and BD-Shallow ConvNets, RF, and ASC were on same level, whereas BD-EEGNet
achieved marginally lower decoding accuracy. SVM indicated the worst performance.


To the best of our knowledge, there is only one other previously published feature-based result for
pathology decoding based on the TUH Abnormal EEG corpus [Lopez de Diego (2017)]. It was achieved
using cepstral coefficients and a CNN+MLP architecture for classification resulting in an accuracy of 78.8%.
We thus increased this feature-based baseline by greater than 5% using RF and ASC, and more than 7%
using RG.
Riemannian-geometry-based classification outperformed all other feature-based models and achieved
85.87% accuracy. We observed that treating covariance matrices with appropriate metrics of their native
space (geometric instead of Euclidean mean) yielded superior performance [S4], which was to be expected

[Barachant et al. (2013)].


12
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _3_ _RESULTS_


This performance of the Riemannian-geometry-based decoding was remarkable considering that the covariance matrix of 21 electrodes had only 231 non-redundant entries. The covariance matrices, as well as
our aggregated high-dimensional feature vectors, did not contain detailed time course information, and, in
both cases, we averaged over the number of crops from which features were extracted. However, the results
demonstrate that there is sufficient information contained in covariance matrices even to outperform all other
tested models using handcrafted features.



![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-14-3.png)





![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-14-1.png)



![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-14-2.png)


































|Target<br>Non-path. Path.<br>139 35 79.8 Prec.<br>[%]<br>11 91 89.5 FOR Metrics<br>92.9 72.1 83.4 Acc.|Col2|
|---|---|
|139<br>11<br>35<br>91<br>79.8<br>89.5<br>83.4<br>92.9<br>72.1<br><br><br><br>|139<br>11<br>35<br>91<br>79.8<br>89.5<br>83.4<br>92.9<br>72.1<br><br><br><br>|
|139<br>11<br>35<br>91<br>79.8<br>89.5<br>83.4<br>92.9<br>72.1<br><br><br><br>|Acc.<br>FOR<br><br>Metrics [%]|



![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-14-7.png)



![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-14-5.png)



![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-14-6.png)





















![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-14-8.png)

























Figure 7: Confusion matrices of all models averaged over independent final evaluation runs are presented
in the upper left 2 _×_ 2 sub-matrix. Specificity (Spec.), sensitivity (Sens.), precision (Prec.), false omission
rate (FOR), and accuracy (Acc.) are indicated. All models determined more false negatives (pathological
examples predicted as non-pathological).


The application of ASC effectively reduces the required amount of time and expert knowledge required
to build and optimize a well-working model and has the ultimate goal of making ML applicable by nonexperts. We can confirm that, given our set of features, ASC achieved competitive results in classifying
EEG pathology, without requiring user interaction. The ensemble that was automatically chosen by ASC
consisted of AdaBoost [Schapire and Freund (2013)] with 78% (66%, 8% and 4%) of ensemble strength,
gradient boosting with 18%, and linear discriminant analysis with 4%.


**3.2** **End-to-end decoding performance**


We present the end-to-end decoding results with deep neural networks in Figure 6, left half. Our overall
best decoding result was 86.16% accuracy obtained by the BD-TCN. This accuracy was extremely close
to the result of 86.57% accuracy previously reported using ChronoNet [Roy et al. (2019)]. The BD-TCN
was followed by BD-Deep4 and BD-Shallow with 84.57% and 84.13% accuracy, respectively. BD-EEGNet
achieved a decoding accuracy of 83.41%. Overall, the networks did not demonstrate as much performance


13
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _3_ _RESULTS_


difference in the CV and final evaluation as the feature-based approaches. For the networks, the differences
were in the range of _−_ 0 _._ 6% to +0 _._ 4% and in the range of _−_ 1 _._ 21% to +4 _,_ 61% for the feature-based approaches.
Again, as in the feature-based approach, we observed more false negatives (Figure 7, top row).
We also tracked learning curves of all applied networks (Figure 8). The loss and misclassification curves
of BD-Deep4 and BD-Shallow are irregular at the start; however, they become smoother after Epoch 20.
BD-EEGNet displayed smooth curves overall, however with the highest loss and misclassification rate. The
curves of the BD-TCN indicate the greatest difference of training to test loss.





![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-15-3.png)


|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|Col13|Col14|Col15|Col16|Col17|Col18|Col19|Col20|Col21|Col22|Col23|BD-Deep4|Col25|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||||||||||||||||||||||||||
||||||||||||||||||||||||||
||||||||||||||||||||||||||




|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|BD-Shallow|
|---|---|---|---|---|---|---|---|---|---|---|
||||||||||||
||||||||||||









Figure 8: Learning curves of investigated network architectures. Smoothing trend can be observed near
Epoch 20, which could be effect of cosine annealing. BD-TCN achieves lowest misclassification rate. Curves
of BD-EEGNet are a sign of underfitting.


The BD-TCN was designed as an alternative to the RNN architectures. Our results indicate that this
model is indeed competitive with ChronoNet, which is a combined ConvNet/RNN architecture, for the
given task in terms of decoding accuracy. The BD-TCN outperformed all other networks, which could be
a consequence of its design and optimization through a neural architecture search [Chrabaszcz _�_ (2018)]. All
other models were originally developed and optimized for other decoding tasks. Their performance in the
present study underlines their general applicability.
The presented learning curves demonstrate astounding differences and we hypothesize that they are
characteristic for the network architectures under investigation. The smoothing of the curves near Epoch 20,
especially observable for BD-Deep4 and BD-Shallow, is likely the effect of cosine annealing updates of the
learning rate. In all models, except BD-EEGNet, we can observe a clear difference between the training and
test loss. We assume that BD-EEGNet is unable to better fit the training data owing to its relatively small
number of parameters (see Table S3); its learning curves indeed indicate signs of underfitting. The opposite,
overfitting, cannot be observed. This could be due to the regularization techniques, i.e., dropout or weight
decay.


14
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _3_ _RESULTS_


**3.3** **Feature-based and end-to-end decoding performances in comparison**


We observed decoding accuracies in the same range using different models and approaches, i.e., ChronoNet
(86.57%), BD-TCN (86.16%), BD-Deep4 (84.57%), ASC (84.71%), RF (84.06%), and RG (85.87%). Our
statistical analysis indicated p-values in the range of 0.37 to 1. There is thus no statistical evidence that one
of these models performed better than the others (Figure 9, lower triangle). Over all pairs of models, the
number of equal classification decisions (ties) ranged from 241–266 of 276 possible (Figure 9, upper triangle).
Several pairs of models actually provided an identical number of errors, i.e., BD-EEGNet, BD-Shallow, and
ASC.



![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-16-8.png)

![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-16-9.png)





















![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-16-13.png)

Figure 9: Results of paired sign tests with equally split ties. Lower triangle indicates p-values for all pairs
of models. The upper triangle displays the number of ties and number of positive and negative signs.
Statistically, there is no evidence to assume that any one model performed better than the other models.


Previous publications [Table 1] have indicated that deep learning typically performs better in decoding
pathology from EEGs using the TUH Abnormal EEG corpus. This is because there is only one published
result using handcrafted features. It appears that this baseline was not particularly strong, which made deep
learning approaches appear superior. However, herein, we determined similar decoding accuracies of featurebased and neural network approaches. Statistically, there is actually no evidence that one of the models
applied for this study performed better than the others . Hence, we conclude that the literature provided a
false picture of reality caused by the omission of comparisons of deep learning with other approaches.


15
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _3_ _RESULTS_


**3.4** **Importance of learned and handcrafted features**


Through our perturbation analysis using the BD-Deep4, we determined correlations with predictions of the
pathological class at temporal electrode locations T3 and T4 when increasing the amplitudes (Figure 10). The
effect was especially prominent in the delta and theta frequency range. Conversely, a decrease in correlation
at occipital electrodes O1 and O2 was the most prominent effect in the alpha frequency range.









![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-17-10.png)



![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-17-11.png)



![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-17-12.png)



![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-17-7.png)





![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-17-8.png)





![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-17-9.png)














|Col1|0.<br>0.<br>0.|
|---|---|
|||
|||



![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-17-6.png)

Figure 10: Input-signal perturbation with BD-Deep4 network displays that higher activity at temporal
electrode locations (T3, T4) is indicative of pathology, especially in low frequency ranges (0–4 Hz and 4–8
Hz). In alpha frequency range, there is negative correlation with pathological class at occipital electrode
locations (O1, O2).


For a comparison with the perturbation analysis, we present the important handcrafted features extracted
in the same frequency ranges using our analysis of feature importance using RF (Figure 11). Features
extracted at temporal electrode T4 in the delta and theta frequency range are most informative, which is
in consensus with the perturbation result. Features extracted at electrode T3, however, are not considered
as informative. In the alpha frequency range, the majority of the informative features were extracted at
occipital electrodes O1 and O2. This, again, is in consensus with the perturbation result.
For a comparison with the perturbation and feature importance analysis, we present a visualization of the
values in the covariance matrices that were mapped to tangent space as used in the Riemannian-gemoetrybased decoding pipeline (Figure 12). It can be observed that the variance extracted at temporal electrodes T3
and T4 is most indicative of a pathology. This is in consensus with the perturbation analysis. Furthermore,
as in the perturbation analysis, variance at electrodes O1 and O2 (and Fp1 and Fp2) are indicative of normal
brain activity. Both observations are underlined by the feature importance analysis.
To further analyze the features, we computed their correlation coefficients and then visualized these.
We display the full feature correlation matrix [Figure 14] and the correlation of FT features extracted from
the delta, theta, and alpha range [Figure 13]. We determined strong correlations, despite feature domain,
frequency band, and electrode recording site.


**3.5** **Time-resolved feature-based decoding**


Inspired by the cropped-decoding setup used in our end-to-end pipeline, we implemented a time-resolved
(non-aggregated) decoding for our feature-based models. However, this did not lead to an increase in decoding
accuracy during CV, which is why we did not investigate this setup any further.


16
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _3_ _RESULTS_









![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-18-8.png)



![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-18-9.png)



![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-18-10.png)



![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-18-5.png)





![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-18-6.png)





![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-18-7.png)















Figure 11: RF feature importance analysis indicates that features extracted at 0–4 Hz and 4–8 Hz at temporal
electrode T4 are most informative. In 8–13 Hz frequency band, occipital electrodes (O1, O2) have highest
importance values.

![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-18-12.png)


Figure 12: Values of covariance matrices mapped to tangent space. Values most indicative of pathological
activity are variance extracted at electrodes T3 and T4. Only variance of O1, O2, Fp1, and Fp2 is indicative
of normal activity.


Given the drastic increase in the amount of data, it should be possible to realize an improvement using
time-resolved decoding, if not here, then for a different task or data set. For the given data, the improvements
could actually be negligible. Because the task is concerned with classifying an EEG recording as either
pathological or non-pathological, there is likely no information in the signals that evolves at a large time
scale. Because the TUH Abnormal EEG Corpus (v2.0.0) is not a seizure or event data set, we assume
that if there exists a continuous alteration in brain activity reflecting a static dysfunction, e.g., related to a
structural brain abnormality, it would be indicated consistently. This is also one of the key assumptions of


17
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _3_ _RESULTS_
















|Col1|1.|
|---|---|
||0.<br>0.<br>|
|||


|A1|x x 0-4 Hz|Col3|
|---|---|---|
|A1<br>A2<br>C3<br>C4<br>Cz<br>F3<br>F4<br>F7<br>F8<br>Fp1<br>p2<br>|~~x~~<br>x<br>x<br>x<br>x<br>x<br>x<br>xx<br>x<br>xx<br>x<br>x<br>x<br>x<br>x<br>x<br>x<br>x<br>x<br>|~~x~~<br>x<br>x<br>x<br>x<br>x<br>x<br>xx<br>x<br>xx<br>x<br>x<br>x<br>x<br>x<br>x<br>x<br>x<br>x<br>|
|A1<br>A2<br>C3<br>C4<br>Cz<br>F3<br>F4<br>F7<br>F8<br>Fp1<br>p2<br>|~~x~~<br>x<br>x<br>x<br>x<br>x<br>x<br>xx<br>x<br>xx<br>x<br>x<br>x<br>x<br>x<br>x<br>x<br>x<br>x<br>|Fp1<br>Fp2<br>Fz<br>O1<br>O2<br>P3<br>P4<br>Pz<br>T3<br>T4<br>T5<br>T6<br>|


|A1|x x 4-8 Hz|Col3|
|---|---|---|
|A1<br>A2<br>C3<br>C4<br>Cz<br>F3<br>F4<br>F7<br>F8<br>Fp1<br>p2<br>|~~x~~<br>x<br>xx<br>x<br>x<br>x<br>x<br>x<br>x<br>xx<br>x<br>x<br>x<br>x<br>x<br>x<br>x<br>x<br>x<br>|~~x~~<br>x<br>xx<br>x<br>x<br>x<br>x<br>x<br>x<br>xx<br>x<br>x<br>x<br>x<br>x<br>x<br>x<br>x<br>x<br>|
|A1<br>A2<br>C3<br>C4<br>Cz<br>F3<br>F4<br>F7<br>F8<br>Fp1<br>p2<br>|~~x~~<br>x<br>xx<br>x<br>x<br>x<br>x<br>x<br>x<br>xx<br>x<br>x<br>x<br>x<br>x<br>x<br>x<br>x<br>x<br>|Fp1<br>Fp2<br>Fz<br>O1<br>O2<br>P3<br>P4<br>Pz<br>T3<br>T4<br>T5<br>T6<br>|


|A1|x x 8-13 Hz|Col3|
|---|---|---|
|A1<br>A2<br>C3<br>C4<br>Cz<br>F3<br>F4<br>F7<br>F8<br>Fp1<br>p2<br>|xx<br>x<br>x<br>x<br>x<br>x<br>x<br>x<br>x<br>x<br>x<br>x<br>x<br>xx<br>x<br>x<br>x<br>x<br>|xx<br>x<br>x<br>x<br>x<br>x<br>x<br>x<br>x<br>x<br>x<br>x<br>x<br>xx<br>x<br>x<br>x<br>x<br>|
|A1<br>A2<br>C3<br>C4<br>Cz<br>F3<br>F4<br>F7<br>F8<br>Fp1<br>p2<br>|xx<br>x<br>x<br>x<br>x<br>x<br>x<br>x<br>x<br>x<br>x<br>x<br>x<br>xx<br>x<br>x<br>x<br>x<br>|Fp1<br>Fp2<br>Fz<br>O1<br>O2<br>P3<br>P4<br>Pz<br>T3<br>T4<br>T5<br>T6<br>|



![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-19-3.png)

![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-19-4.png)

![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-19-5.png)

Figure 13: Feature correlation analysis in frequency bands 0–4, 4–8, and 8–13 Hz. For every electrode (row),
most highly correlated electrode is marked with a white cross. In frequency band 0–4 Hz, features extracted
at T3 are most correlated with those extracted at T4, which could explain the pattern observed in Figure 11.
In the 4–8 Hz frequency region, all features appear to be highly correlated with exceptions such as F7 or F8.
In the 8–13 Hz region, features of occipital temporal and parietal region are especially highly correlated.


our aggregated decoding approach, which performed as well as the ConvNets [see 3.1]. If this assumption did
not hold, an aggregation, especially using the median as an aggregation function, would result in smoothing
of the effect caused by the pathology. In a different data set, where signals change over a larger time scale,
a time-resolved decoding could result in superior decoding performance. However, one must consider the
challenges that are posed by time-resolved feature-based decoding. In our study, the amount of data increased
by a factor of approximately 200 compared to aggregated decoding.


**3.6** **Effect of patient-specific information on decoding accuracies**


We investigated the influence of so-called meta features, i.e., age and gender of patients, with respect to
the decoding accuracies. Therefore, we added the age and gender of the patients to our feature vectors and
as additional network channels to our BD-TCN. Classification accuracy improved only marginally during
CV, e.g., RF CV accuracy increased by 0.15% (from 83.1% to 83.25%) by adding age and gender. For this
reason, we did not further pursue the use of these meta features. Our result is in consensus with a recent
publication, where the authors attempted to combine neural networks and the age information of patients to
improve the decoding of pathology from EEGs [Van Leeuwen et al. (2019)]. They also found only marginal,
insignificant improvements (+0 _._ 07 area under the receiver operating characteristic curve).
As clinicians have access to diverse information regarding patients that are not included in the EEG
recordings, such as age, gender, current physical and mental condition, patient history, ongoing medical
treatment, and more. All of this could have a role in their diagnosis or unconsciously introduce a bias. For
example, we have seen several physician reports in the TUH Abnormal EEG corpus (more than 100) with
the comment “IMPRESSION: Normal EEG for this age” or similar. This is clearly a relative statement by
the clinician relying on age information that our models do not have available to find a diagnosis.
Moreover, there is clearly a bias (patient age) in the data set that can be retrieved from the histogram

[Figure 5]. In the data set pathologies certainly appear more frequent with higher age. Where this is a
justifiable representation of reality, it could unconsciously bias clinicians to diagnose EEG recordings of
patients with a high age rather as pathological. Although our experiments did not indicate a substantial


18
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _3_ _RESULTS_



![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-20-6.png)





![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-20-4.png)

Figure 14: Full feature correlation matrix of all implemented features of domains CWT, DWT, FT, Riemannian, Connectivity, and Time. Features are sorted by feature domain, alphabetically by feature name,
ascending by frequency band and alphabetically by electrode location. Strong correlations can be observed
across different features within same and between other domains.


improvement when adding patient age and gender in the classification process, the suitable inclusion of
patient-specific information from physician reports could improve classification accuracies.
Furthermore, knowledge of other findings related to a patient could unconsciously bias clinicians to be
overly sensitive to minimal changes in the EEG. For example, small changes in an EEG might not be
considered as indicative of a pathology on their own, however, in combination with the knowledge of a lesion
based on imaging techniques the EEG could be considered as pathological. Access to different amounts of


19
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _3_ _RESULTS_


information could be one explanation for the observation of more false negatives than false positives across
all models [Figure 7].


**3.7** **Ensemble decoding performance**


Our analysis of prediction correlations revealed that the CV predictions of all our models were highly correlated (Spearman correlation of up to 0.96) and indicated a large ratio (up to 61%) of non-overlapping label
errors [Figure 15].


20
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _4_ _DISCUSSION_



![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-22-5.png)

![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-22-6.png)



















![](literature/markdown/gaemin-2020/GAEMIN-2020.pdf-22-10.png)

Figure 15: Analysis of CV predictions. In lower triangle, Spearman correlation of pairs of model predictions
is displayed. In upper triangle, we added ratio of non-overlapping label errors. Riemannian-geometry-based
decoding and BD-Deep4 indicate greatest opportunity for improvement as their predictions have a correlation
of 0.82 and ratio of non-overlapping label errors of 0.61.


We present the results of our two ensemble approaches in Table 4. The combination of the models BDDeep4, RF, and RG had the highest ratio of non-overlapping CV label errors (336 errors, ratio of 44.56%),
which is why we selected them for majority vote ensembling. Automatic ensembling based on auto-sklearn
chose every model except the SVM and computed optimal weights based on the CV predictions [Figure 4].
Whereas the auto-sklearn ensemble resulted in the overall best CV accuracy (86.23%), neither ensembling
based on majority voting (85.51%) nor automatic ensemble selection (85.14%) resulted in an improvement
over best single-model performance (BD-TCN: 86.16%) in the final evaluation (see Figures 6, 7).

### **4 Discussion**


In this study, we achieved a feature-based decoding accuracy of 85.87% using Riemannian-geometry-based
decoding [Section 3.1] which is greater than 7% higher than the previous feature baseline of 78.8% by Lopez de
Diego (2017). Our BD-TCN achieved an even superior decoding accuracy of 86.16% [Section 3.2]. We found
no statistical evidence that either model under investigation – feature-based or neural network – performed
better than the others [Section 3.3]. We observed that temporal EEG dynamics in slow frequency ranges


21
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _4_ _DISCUSSION_


**Majority Vote** **Auto-sklearn**
Model Weight Model Weight
BD-Deep4 1 BD-Deep4 0.048
RF 1 BD-Shallow 0.286

RG 1 BD-TCN 0.190

BD-EEGNet 0.238

RF 0.190

RG 0.048
CV [%] 84.61 86.23
Final evaluation [%] 85.51 85.14


Table 4: Result of ensembling investigation indicating models, weights, and performances of two ensembles.
One based on majority voting and one automatically selected by auto-sklearn. Neither ensemble improved
compared to best single-model performances.


were informative for detecting pathological changes, and that this information was used in both pipelines

[Section 3.4]. Moreover, our feature correlation analysis revealed high correlations despite feature domain,
frequency band, and electrode recording site. Neither our time-resolved feature-based decoding [Section 3.5],
nor the inclusion of age and gender of patients in the decision processes resulted in a substantial improvement
of decoding accuracy [Section 3.6]. Finally, we determined that ensembling with auto-sklearn can improve
classification accuracy in CV [Section 3.7]; however, not in the final evaluation.


**4.1** **Proposed feature-based pathology decoding concept**


For our study, we aimed at creating a strong feature-based decoding pipeline for a comparison with neural
networks. Therefore, our concept for feature-based decoding involved testing I) a large set of EEG features
of different feature domains (in the present study time, amplitude, phase, and connectivity) and II) multiple
classifiers including ensembles of classifiers (in the present study RFs, SVMs, and ASC). In particular, it was
important to us to also include recent state-of-the-art feature-based methods such as Riemannian-geometrybased classification [Lotte et al. (2018)].
We found significant differences of our concept to those presented in the literature. Where we computed
8633 features of 50 feature types and six domains [see Table 3], typically far smaller feature sets were used
in the literature. For example, Hosseinifard et al. (2013) extracted, exclusively, the total power from the
theta, alpha, and beta frequency bands to decode depression. Similarly, Lopez de Diego (2017) extracted a
single feature type (cepstral coefficients) that originated from the field of speech recognition to decode EEG
pathology. An example of a study with a larger amount of feature types is the work of Cai et al. (2016). They
extracted 16 feature types including amplitude, time, and connectivity measures to detect mild depression.
In our present study, however, we computed an even larger feature set with more than twice the number of
feature types [Table 3].
In other tasks, such as in the movement of the left hand, right hand, and feet motor decoding applications, it is generally assumed that the primary source of information is contained in the signal amplitudes

[Schirrmeister et al. (2017b)]. Typically, there are a small number of target classes (3–4), which must be
modeled. For pathology decoding, conversely, the most informative feature domain or type is not _a priori_
known. Furthermore, it is necessary to model a larger number of pathologies. It cannot be assumed that the
pathologies included in the TUH Abnormal EEG Corpus (v2.0.0) can be described by a single feature type.
Therefore, in our concept, we did not _a priori_ exclude any feature domains or types.


22
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _4_ _DISCUSSION_


In our view, the presented concept is not specific to EEG pathology decoding; rather, it is applicable
to a wide range of other EEG decoding tasks. It could well be possible that approaches based on a single
feature type, e.g., motor decoding based on amplitude features, could be improved by combining them with
different feature types, such as measures of connectivity.


**4.2** **Proposed end-to-end pathology decoding concept using deep neural net-**
**works**


Similar to the feature-based concept, our aim was also to create a strong end-to-end pipeline. By end-to-end,
we refer to the decoding of raw or minimally preprocessed data, unlike decoding based on explicitly extracted,
handcrafted features. Recently, end-to-end methods have achieved powerful results in EEG decoding [Craik
et al. (2019)]. In the present study, we applied the two most widely used, well benchmarked, and open source
network architectures in EEG decoding: BD-Deep4 [Schirrmeister et al. (2017b)] and a reimplementation of
EEGNet [Lawhern et al. (2018)] as implemented in the Braindecode toolbox. Furthermore, we also investigated the application of the BD-TCN, an EEG-optimized TCN architecture. The general TCN architecture
was specifically designed to model sequential data and has outperformed RNNs in machine translation and
audio synthesis tasks [Bai et al. (2018)]. Moreover, we compared to the results of ChronoNet, a CNN/RNN
architecture, reported in the literature [Roy et al. (2019)], as it is among the state-of-the-art in EEG pathology decoding. Finally, we also applied BD-Shallow, which is a special case inasmuch as it was specifically
designed to extract band power features. It is, therefore, between the classical feature-based and end-to-end
decoding philosophies. In summary, the investigated architectures demonstrated significant differences including network archetype (ConvNet, TCN, RNN), parameter count (see Table S3), and number of layers
(Figures 2–4).


**4.3** **Feature-based pathology decoding accuracies**


Riemannian-geometry-based decoding resulted in an accuracy of 85.87%, which was the best feature-based
decoding result. Interestingly, in our study, we observed a narrow range of feature-based decoding accuracies
of 81 to 86% across different classifiers [see Figures 6, 7]. Actually, no statistically significant difference
of accuracies of all presented feature-based models could be detected [see Figure 9]. Previously, Lopez de
Diego (2017) reported an accuracy of 78.8% based on a single feature type and a CNN/MLP architecture
for classification. Both, the size of the feature sets and choice of the decoders could explain the difference in
accuracy. To the best of our knowledge, the study of Lopez de Diego (2017) is the only previously published
feature-based study on EEG pathology decoding. Compared to this previous feature-based state-of-the-art,
our findings demonstrate that substantially higher feature-based decoding accuracies are possible using the
proposed approach.


**4.4** **Deep end-to-end pathology decoding accuracies**


End-to-end methods yielded accuracies in the range of 82–86% [see Figures 6, 7]. Astonishingly, this range
was extremely similar to the range of accuracy obtained with the feature-based pipeline, which was 81–86%.
The EEG-optimized TCN was our best-performing neural network architecture achieving an accuracy of
86.16%. Interestingly, [Van Leeuwen et al. (2019)] also reported an accuracy of approximately 82% using
BD-Deep4 to decode pathology; however, this was based on a different EEG data set. Their data set is
comprised of more examples than the TUH Abnormal EEG Corpus (v2.0.0); however, it is not publicly
available. Similar to the feature-based methods for the architectures under investigation, no statistically


23
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _4_ _DISCUSSION_


significant difference in decoding accuracy could be detected [see Figure 9]. Compared to our BD-TCN,
ChronoNet achieved a marginally higher decoding accuracy of 86.56% [Roy et al. (2019)]. In line with our
present findings, in a previous study, Heilmeyer et al. (2018) also found no statistically significant difference in
accuracies comparing BD-Deep4 with BD-EEGNet in a large-scale benchmark test across different tasks and
data sets. In the following, we now further discuss the virtually identical accuracy range of our feature-based
and end-to-end pipelines.


**4.5** **Deep end-to-end versus feature based-decoding accuracies**


A main finding of our present study, together with the results of Van Leeuwen et al. (2019) and Roy et al.
(2019) is that EEG pathology decoding accuracies lie in a narrow range of 81–86%, even though we compared
a broad range of:


_•_ **Analysis strategies** including deep-end-to-end, feature-based, automated ML, and based on RG;


_•_ **Network archetypes** including ConvNet, TCN, and RNN;


_•_ **Network architectures** including BD-Deep4, BD-TCN, BD-EEGNet, BD-Shallow, and ChronoNet;


_•_ **Feature-based classifiers and ensembles** including RF, SVM, and ASC, and;


_•_ **Data sets** including the Temple University Hospital Abnormal EEG Corpus (v2.0.0) and the data set
used by Van Leeuwen et al. (2019).


Importantly, this range was also considerably below a perfect classification score (100%). Decades of
previous EEG research have indicated that inter-rater reliability in EEG diagnostics is only moderate [Grant
et al. (2014), Houfek and Ellingson (1959), Rose et al. (1973)], which ultimately results in label noise. Regarding label noise, we refer to expert mistakes in diagnosing the EEG recordings as either pathological
or non-pathological, which has a number of mutually related consequences [Fr´enay and Verleysen (2013)]:
decrease of decoding performance, increase of required amount of data to achieve acceptable decoding performance, and increase of model complexity to properly fit the data. Furthermore, label noise complicates the
identification of relevant features [Fr´enay and Verleysen (2013)]. Importantly, in our setting, low inter-rater
agreement and the resulting label noise imposed a limit on the theoretically achievable decoding accuracies
because we were required to evaluate against the noisy labels within our separate, final evaluation set. Moreover, we did not have access to any rater-independent ground truth [14] . Interestingly, inter-rater agreement in
binary classification of EEGs into pathological and non-pathological has been reported as 86–88% [Houfek
and Ellingson (1959), Rose et al. (1973)], although these scores were based on EEG ratings of only two neurologists. Given these numbers, it would appear to be a possibility that EEG pathology decoding accuracies
as observed herein and previously by Van Leeuwen et al. (2019), Schirrmeister et al. (2017a), and Roy et al.
(2019) at approximately 86% could have approached the theoretical optimum imposed by label noise. This
proposed hypothesis could be tested in the future; however, it would involve a considerable effort. It would
require both a large data set as used in the present study and independent ratings of multiple EEG experts.
A massive amount of EEG data is waiting in the archives of medical centers to be used. As end-to-end
approaches are typically data intense, a larger amount of training data could help to improve generalization
further. Moreover, in traditional feature-based approaches, more data would probably illicit positive effects,
as more data in ML is typically favorable over more complex classification algorithms [Halevy et al. (2009)].


14 One can design alternative decoding tasks different from pathology decoding based on the TUH Abnormal EEG Corpus,
such as the decoding of patient gender or age.


24
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _4_ _DISCUSSION_


Furthermore, a labeling of EEG recordings as pathological or non-pathological through an ensemble of considerable number of neurologists and/or epileptologists would be a significant beginning to improve label
quality. The inter-rater agreement scores that result from the ensemble could then be included in the data
set on a per-recording basis, such that they can be included in a detailed analysis.
In the case where the hypothesis is incorrect and the theoretically optimal EEG pathology decoding
accuracy is higher, we see two possible, nonexclusive causes. The first is that inter-rater reliability of the
current data sets is higher than the numbers typically reported in the literature [Houfek and Ellingson (1959),
Rose et al. (1973)]. The second is that all the methods investigated to date did not extract or use certain
features and information that was used by the physicians to determine a diagnosis. In the first case, the
question arises why neither the end-to-end nor the feature-based pipeline could better fit and predict the
data. In the second case, the question arises as to what additional source of information was used by the
physicians and how it could be included to enhance performance. Both cases would open up new, interesting
research questions.


**4.6** **Learned versus handcrafted features**


Based on our feature visualizations, we determined that features extracted in the theta and delta range from
the temporal electrode locations are considered informative. Knowing that epilepsy is statistically one of
the most common disorders of the brain [Thijs et al. (2019)] and that temporal lobe epilepsy is the most
prominent epilepsy [Helmstaedter and Elger (2009)], this could be a reason why this region is important
in determining pathology in all decoding pipelines. Note that although we know epilepsy is one of the
pathologies included in the data set, we neither know the exact number of occurrences nor how many of
those suffer from temporal lobe epilepsy.
Interestingly, only features extracted at electrode T4 are considered important in the theta band based
on the feature importance analysis [Figure 11]. This is in strong contrast to the network perturbation result

[Figure 10] and covariance matrix visualization [Figure12], where both hemispheres were considered equally
informative in this range. Given the mechanisms of a decision tree, we assume that the tree chose features
extracted at T4 in the theta band early in the decision process, because they are informative. Features
extracted at T3 in the same frequency band were then not selected for further splitting of examples because
they did not provide additional information. Hence, we assumed that the features were highly correlated.
Our feature correlation analysis [Figure 13] revealed several strong, positive correlations of features extracted at different electrode locations. Indeed, features extracted at T3 were most correlated with features
extracted at T4 (correlation coefficient approximately 0.9) in frequency band 4–8 Hz. We actually observed
this effect of strong correlations across several of our handcrafted features, despite feature domain, electrode
location, and frequency band [Figure 14].
The covariance matrix visualization [Figure 12] supported the findings of our perturbation and feature importance analysis. Features extracted from temporal electrode locations were most informative for decoding
pathology, especially in the delta and theta frequency range.
The result of the perturbation [Figure 10] and feature importance analysis [Figure 11] in the 8–13 Hz
range indicated that occipital electrodes were also extremely informative. This is again supported by the
covariance matrix visualization [Figure 12]. The variance of electrodes O1 and O2 (and also Fp1 and Fp2)
are the only variances that were indicative of normal brain activity. We explain this by the prominent alpha
rhythm in adults in a resting state. Given the perturbation result, lower amplitudes are anti-correlated with
pathology; or, in other words, higher amplitudes are correlated with normal brain activity.
Through the comparison of our analyses, we determined that the first visualization of the feature importance [Figure 11] was misleading, owing to strong feature correlations. Typically, ease of interpretation is


25
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _4_ _DISCUSSION_


considered an advantage of feature-based approaches over end-to-end approaches; however, we determined
that there are also limitations to this interpretability. Pitfalls with RF feature correlations were also described
by Altmann et al. (2010).


**4.7** **Beyond automated binary EEG pathology diagnostics**


In general, the task we addressed (classifying EEG recordings as either pathological or non-pathological)
is especially difficult. The TUH Abnormal EEG data set does not only contain multiple, highly different
pathologies including, but not limited to, Alzheimer’s disease, strokes, depression, and epilepsy (which are
difficult to model), but also there is only one common label for all of them. Hence, it can be interpreted
as a combination of several decoding tasks. Presumably, every individual decoding task has a non-convex
loss landscape. The performance of deep neural networks heavily depends on the optimization of the loss
function and hence finding a minimum in the loss landscape [Li et al. (2018)]. A landscape that arises from
the combination of tasks could be even more complex and, therefore, be more difficult to optimize.
To investigate whether the decoding of individual pathologies is easier and offers a path towards automatic EEG diagnostics beyond binary classification, we initiated work on restructuring the physician reports
included in the TUH Abnormal EEG Corpus to a tabular format which is a more machine and user-friendly
representation. The code for restructuring is uploaded to our repository [15] . We are seeking support to further
specify the diagnoses of patients (to ICD-10 codes [World Health Organization (1992)]) whose recordings
were labeled pathological. Moreover, we aim to find a suitable method to encode patient histories and
ongoing medical treatment, such that they can be used in classification.
Although we are extremely interested in further specifying the diagnoses of patients included in the
physician reports as a basis for advanced pathology decoding, we doubt its clinical usefulness. Owing to
their ease of application, low cost, wide availability, and non-invasive nature, EEGs are a valuable screening
method. Typically, when an EEG recording is found to be pathological, multiple other clinical sources, i.e.,
medical imaging such as magnetic resonance imaging (MRI), are involved to actually determine a diagnosis.
In the majority of cases, an EEG is not used (and not sufficient) to diagnose a neurological disease or disorder,
as an occurrence of pathological change is seldom specific for one disease or disorder. From our point of view,
a reasonable extension of the given decoding task could be to classify recordings as either normal, epileptic,
or differently pathological. As epilepsy is one of the most common disorders of the brain [Thijs et al. (2019)],
this classification would further support neurologists in screening patients using EEGs.


**4.8** **Clinical usefulness of current decoders of EEG pathology**


Everyday medical applications typically require higher accuracy than the current state-of-the-art in EEG
pathology decoding to be accepted. However, decoding pipelines with an accuracy in the current range can be
valuable. For example, they could make EEG diagnostics available to patients that cannot attend specialized
centers. This includes wide areas of developing countries where specialized centers and neurological experts
are rare. Approximately 50 million people worldwide suffer from epilepsy [World Health Organization (2019)],
of which the vast majority live in developing countries [World Health Organization (2019), Singh and Trevick
(2016)]. In these countries, in addition to their disease or disorder, patients frequently suffer from social
stigma [World Health Organization (2019), Newton and Garcia (2012)] owing to missing diagnoses and
inexperience in addressing those diseases and disorders. In our opinion, although diagnostic accuracy is at
approximately 86%, an automatic diagnosis is better than not being diagnosed at all. The pipelines could


15 available for download at `[https://github.com/gemeinl/auto-eeg-diagnosis-comparison](https://github.com/gemeinl/auto-eeg-diagnosis-comparison)`


26
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _4_ _DISCUSSION_


be used as a prescreening method, which could recommend a visit to a specialized center in the case of the
detection of pathological activity.


**4.9** **Implications for EEG decoding accuracy evaluation in general**


Our findings of statistically similar decoding accuracies of different networks and classifiers has implications
for other publications. EEG decoding papers based on deep end-to-end learning frequently compare their
results to only (rather) simple feature-based approaches or exclusively to other deep end-to-end learning
results. For example, for the pathology decoding task based on the TUH Abnormal EEG corpus, all publications based on deep end-to-end learning compared to the result of Lopez de Diego (2017). This leads
to the impression that deep neural networks heavily outperform feature-based approaches. However, in this
study, we demonstrated that with a somewhat elaborate feature-based approach, one can achieve decoding
results similar to deep end-to-end methods [Figures 6, 7]. To be more precise, there is actually no statistical
evidence that the investigated networks perform any better than the feature-based approaches [Figure 9]. We
therefore emphasize once more, that fair comparisons to strong baselines are essential to assess the quality
of decoding results. This does not only hold for EEG pathology decoding tasks, but also for EEG decoding
tasks in general. Moreover, the necessity of comprehensive comparisons holds for all areas of application of
ML.


**4.10** **Public availability of resources and reproducibility**


The availability of code that can be used to independently reproduce the published results is currently the
only method to truly assess the scientific quality and generalizability of the proposed approaches. To the
best of our knowledge, there are only six other published results for general pathology decoding from EEGs,
five of which are based on the TUH Abnormal EEG Corpus (Table 1). Van Leeuwen et al. (2019) have used
and adapted our BD-Deep4 network and applied both the original and adapted version to the same task on
a different, even larger data set. Their results indicate that both versions yield identical decoding results in a
similar range (82% accuracy) to what we present in this study. Furthermore, they also investigated the effect
of including patient age in the classification process and determined only marginal improvements, which is
in consensus with our observations [see Effect of patient-specific information on decoding accuracies]. First,
this underlines the general applicability of our BD-Deep4; second, it serves as a reproduction study of our
results. To improve the reproducibility in EEG decoding further, we have uploaded the resources [16] of our
previous study [Schirrmeister et al. (2017a)] and also uploaded the resources of our current study [17] .


**4.11** **Potential improvements of the decoding pipelines**


Although we implemented a large set of features of different domains for this study, this collection is not close
to completion. There are probably an infinite number of features one could implement, e.g., in the domain
of connectivity features one could additionally investigate the usage of cross-correlation, cross-coherence,
mutual information, omega complexity, s-estimator, and global field synchronization [Jalili et al. (2013)]. We
have already attempted to add the gender and ages of the patients to improve classification [3.6]. In clinical
diagnostics, physicians have access to even more information such as medical patient history and ongoing
medication. It is an open challenge as to how to include this information in the decision process.


16 `[https://github.com/robintibor/auto-eeg-diagnosis-example](https://github.com/robintibor/auto-eeg-diagnosis-example)`
17 `[https://github.com/gemeinl/auto-eeg-diagnosis-comparison](https://github.com/gemeinl/auto-eeg-diagnosis-comparison)`


27
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _5_ _OUTLOOK AND CONCLUSION_


With extremely high-dimensional feature-spaces as presented in this study, it is natural to rethink dimensionality reduction methods. A small feature dimension is favorable because it yields shorter learning times
and makes interpretation easier. Although our preliminary feature selection with PCA resulted in a decrease
of decoding performance, there are several other approaches to be investigated, including independent component analysis [Comon (1994)] (ICA) or tensor decomposition [Sidiropoulos et al. (2017)]. Furthermore,
one could also attempt to enhance signal quality by applying a source reconstruction method [Michel et al.
(2004)] prior to the extraction of the features and classification. We have observed that features extracted
from temporal electrode locations were highly informative for the decoding of EEG pathology [3.4. A more
precise localization of signals could also improve classification accuracy.
As in the implementation of features, there are numerous other feature-based classifiers available. ASC
automatically selected models that we did not choose ourselves [Section 3.7], i.e., AdaBoost and Gradient
Boosting. Both classifiers, however, are frequently implemented with decision trees that also form the basis
of RFs. It could be worth further investigation into the application of other classifiers. A specific case is
when performing time-resolved feature-based decoding [Section 3.5], where the models chosen for the present
study could not yet benefit from the drastic increase of data.
Finally, one could run a pipeline search optimization based on automated ML [Hutter et al. (2019)]. This
could not only include feature scaling, selection of classifiers, and optimization of their hyperparameters as
executed by ASC and as already performed for the present study. One could also attempt to optimize the
hyperparameters for feature extraction itself, such as frequency bands, aggregation function, window length,
window function, and others. We are convinced that a systematic optimization of these choices could lead
to even better-performing feature-based EEG decoding results.
In the huge search space of network architectures, the models investigated in this study possibly lie in a
subspace that contains well-performing architectures for this task. Most likely, these architectures are not
yet optimal to decode EEG pathology. Many research groups are now promoting the development of neural
architecture search (NAS) [Elsken et al. (2019)] to address the concern that handcrafting features is now
being replaced by architecture crafting. NAS is achieving rapid progress and we assume that it will spawn
even better-performing architectures in the close future.

### **5 Outlook and Conclusion**


We emphasize once more that the discussed study with a large data set and improved inter-rater quantification
should be performed to test our hypothesis of an accuracy limit in EEG pathology decoding at approximately
90%. In addition to the possibilities for improvements discussed above, data augmentation could be another.
Although augmentation for EEGs is not as intuitive as for other types of signals, the first promising results
used cutout on raw EEG signals [Pereira et al. (2018)] or rotation of electrode recording sites [Krell et al.
(2018)]. Augmentation could also be combined with automated ML [Cubuk et al. (2018), Lim et al. (2019)]
to further advance the data intense end-to-end models.

To circumvent the consequences of label noise in EEG pathology decoding, instead we propose to decode
I) the gender of patients to better assess the potentials of feature-based and end-to-end pipelines, and II)
the age of patients to use the gap of chronological age to predicted brain age as an alternative source for
indication of pathology. In the literature this gap and its estimation based on MRI scans is referred to
brainAGE [Franke (2013), Franke et al. (2010)].
Based on our insights obtained through the present study, we see a promising future for automated
EEG diagnostics. A well-working pipeline that implements the mentioned options for improvements could
be helpful in the interpretation of EEG recordings. It could not only make EEG diagnostics available to
patients that cannot attend specialized centers, but could also allow for earlier detection of pathologies on the


28
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _REFERENCES_


same level as ensembles of human experts, and thereby somewhat reduce the global burden of neurological
diseases and disorders.

### **Acknowledgements**


This work was supported by the Graduate School of Robotics, Georges-K¨ohler-Allee 80, 79110, Freiburg,
Germany and the State Graduate Funding Program of Baden-W¨urttemberg, Germany.

### **Conflict of interest**


The authors declare no competing financial interests.

### **Data and code availability statements**


The TUH Abnormal EEG Corpus [Lopez de Diego (2017)] used for our study is a subset of the TUH EEG
Corpus [Obeid and Picone (2016), DOI: 10.3389/fnins.2016.00196]. Both data sets are publicly available for
download upon registration at `www.isip.piconepress.com/projects/tuh_eeg/html/downloads.shtml` .
The code used for our study relies on the open source toolboxes Braindecode ( `github.com/TNTLFreiburg/`
`braindecode` ) and Brainfeatures ( `github.com/TNTLFreiburg/brainfeatures` ). Code specific to the experiments performed for our study was uploaded to `github.com/gemeinl/auto-eeg-diagnosis-comparison` .

### **References**


Albert, B., Zhang, J., Noyvirt, A., Setchi, R., Sjaaheim, H., Velikova, S., and Strisland, F. (2016). Automatic
EEG processing for the early diagnosis of traumatic brain injury. _Procedia Computer Science_, 96:703–712.


Alhussein, M., Muhammad, G., and Hossain, M. S. (2019). EEG pathology detection based on deep learning.
_IEEE Access_, 7:27781–27788.


Altmann, A., Tolo¸si, L., Sander, O., and Lengauer, T. (2010). Permutation importance: a corrected feature
importance measure. _Bioinformatics_, 26(10):1340–1347.


Amin, S. U., Hossain, M. S., Muhammad, G., Alhussein, M., and Rahman, M. A. (2019). Cognitive smart
healthcare for pathology detection and monitoring. _IEEE Access_, 7:10745–10753.


Ang, K. K., Chin, Z. Y., Zhang, H., and Guan, C. (2008). Filter bank common spatial pattern (FBCSP) in
brain-computer interface. In _2008 IEEE International Joint Conference on Neural Networks (IEEE World_
_Congress on Computational Intelligence)_, pages 2390–2397. IEEE.


Bai, S., Kolter, J. Z., and Koltun, V. (2018). An empirical evaluation of generic convolutional and recurrent
networks for sequence modeling. _[arXiv preprint arXiv:1803.01271](http://arxiv.org/abs/1803.01271)_ .


Balli, T. and Palaniappan, R. (2009). A combined linear & nonlinear approach for classification of epileptic
EEG signals. In _2009 4th International IEEE/EMBS Conference on Neural Engineering_, pages 714–717.
IEEE.


29
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _REFERENCES_


Barachant, A., Bonnet, S., Congedo, M., and Jutten, C. (2013). Classification of covariance matrices using
a Riemannian-based kernel for BCI applications. _Neurocomputing_, 112:172–178.


Biswal, S., Kulas, J., Sun, H., Goparaju, B., Westover, M. B., Bianchi, M. T., and Sun, J. (2017). SLEEPNET: automated sleep staging system via deep learning. _[arXiv preprint arXiv:1707.08262](http://arxiv.org/abs/1707.08262)_ .


Boser, B. E., Guyon, I. M., and Vapnik, V. N. (1992). A training algorithm for optimal margin classifiers.
In _Proceedings of the fifth annual workshop on Computational learning theory_, pages 144–152. ACM.


Breiman, L. (2001). Random forests. _Machine learning_, 45(1):5–32.


Cai, H., Sha, X., Han, X., Wei, S., and Hu, B. (2016). Pervasive EEG diagnosis of depression using deep belief
network with three-electrodes EEG collector. In _2016 IEEE International Conference on Bioinformatics_
_and Biomedicine (BIBM)_, pages 1239–1246. IEEE.


Caruana, R., Niculescu-Mizil, A., Crew, G., and Ksikes, A. (2004). Ensemble selection from libraries of
models. In _Proceedings of the twenty-first international conference on Machine learning_, page 18. ACM.


Chrabaszcz, P. (2018). Neural architecture search. Master’s thesis, Albert Ludwig University Freiburg. _�_


Comon, P. (1994). Independent component analysis, a new concept? _Signal processing_, 36(3):287–314.


Craik, A., He, Y., and Contreras-Vidal, J. L. (2019). Deep learning for electroencephalogram (EEG) classification tasks: a review. _Journal of neural engineering_, 16(3):031001.


Cubuk, E. D., Zoph, B., Mane, D., Vasudevan, V., and Le, Q. V. (2018). Autoaugment: Learning augmentation policies from data. _[arXiv preprint arXiv:1805.09501](http://arxiv.org/abs/1805.09501)_ .


Dixon, W. J. and Mood, A. M. (1946). The statistical sign test. _Journal of the American Statistical_
_Association_, 41(236):557–566.


Elsken, T., Metzen, J. H., and Hutter, F. (2019). Neural architecture search: A survey. _Journal of Machine_
_Learning Research_, 20(55):1–21.


Esteller, R., Echauz, J., Tcheng, T., Litt, B., and Pless, B. (2001). Line length: an efficient feature for
seizure onset detection. In _2001 Conference Proceedings of the 23rd Annual International Conference of_
_the IEEE Engineering in Medicine and Biology Society_, volume 2, pages 1707–1710. IEEE.


Feurer, M., Klein, A., Eggensperger, K., Springenberg, J., Blum, M., and Hutter, F. (2015). Efficient
and robust automated machine learning. In _Advances in Neural Information Processing Systems_, pages
2962–2970.


Franke, K. (2013). _BrainAge: a novel machine learning approach for identifying abnormal age-related brain_
_changes_ . PhD thesis, University of Zurich.


Franke, K., Ziegler, G., Kl¨oppel, S., Gaser, C., Initiative, A. D. N., et al. (2010). Estimating the age of
healthy subjects from T1-weighted MRI scans using kernel methods: exploring the influence of various
parameters. _Neuroimage_, 50(3):883–892.


Fr´enay, B. and Verleysen, M. (2013). Classification in the presence of label noise: a survey. _IEEE transactions_
_on neural networks and learning systems_, 25(5):845–869.


30
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _REFERENCES_


Gemein, L. A. W. (2017). Automated EEG diagnosis. Master’s thesis, Albert Ludwig University Freiburg.


Giri, E. P., Fanany, M. I., Arymurthy, A. M., and Wijaya, S. K. (2016). Ischemic stroke identification based
on EEG and EOG using 1D convolutional neural network and batch normalization. In _2016 International_
_Conference on Advanced Computer Science and Information Systems (ICACSIS)_, pages 484–491. IEEE.


Grant, A. C., Abdel-Baki, S. G., Weedon, J., Arnedo, V., Chari, G., Koziorynska, E., Lushbough, C., Maus,
D., McSween, T., Mortati, K. A., et al. (2014). EEG interpretation reliability and interpreter confidence:
a large single-center study. _Epilepsy & Behavior_, 32:102–107.


Halevy, A., Norvig, P., and Pereira, F. (2009). The unreasonable effectiveness of data. _IEEE Intelligent_
_Systems_, 24(2):8–12.


Hammer, J., Fischer, J., Ruescher, J., Schulze-Bonhage, A., Aertsen, A., and Ball, T. (2013). The role
of ECoG magnitude and phase in decoding position, velocity, and acceleration during continuous motor
behavior. _Frontiers in neuroscience_, 7:200.


Hartmann, K. G., Schirrmeister, R. T., and Ball, T. (2018). Hierarchical internal representation of spectral
features in deep convolutional networks trained for EEG decoding. In _2018 6th International Conference_
_on Brain-Computer Interface (BCI)_, pages 1–6. IEEE.


Heilmeyer, F. A., Schirrmeister, R. T., Fiederer, L. D., Volker, M., Behncke, J., and Ball, T. (2018). A largescale evaluation framework for EEG deep learning architectures. In _2018 IEEE International Conference_
_on Systems, Man, and Cybernetics (SMC)_, pages 1039–1045. IEEE.


Helmstaedter, C. and Elger, C. E. (2009). Chronic temporal lobe epilepsy: a neurodevelopmental or progressively dementing disease? _Brain_, 132(10):2822–2830.


Hinton, G., Deng, L., Yu, D., Dahl, G., Mohamed, A.-r., Jaitly, N., Senior, A., Vanhoucke, V., Nguyen, P.,
Kingsbury, B., et al. (2012). Deep neural networks for acoustic modeling in speech recognition. _IEEE_
_Signal processing magazine_, 29.


Hjorth, B. (1970). EEG analysis based on time domain properties. _Electroencephalography and clinical_
_neurophysiology_, 29(3):306–310.


Hosseinifard, B., Moradi, M. H., and Rostami, R. (2013). Classifying depression patients and normal subjects using machine learning techniques and nonlinear features from EEG signal. _Computer methods and_
_programs in biomedicine_, 109(3):339–345.


Houfek, E. E. and Ellingson, R. J. (1959). On the reliability of clinical EEG interpretation. _The Journal of_
_nervous and mental disease_, 128(5):425–437.


H¨ugle, M., Heller, S., Watter, M., Blum, M., Manzouri, F., Dumpelmann, M., Schulze-Bonhage, A., Woias,
P., and Boedecker, J. (2018). Early seizure detection with an energy-efficient convolutional neural network
on an implantable microcontroller. In _2018 International Joint Conference on Neural Networks (IJCNN)_,
pages 1–7. IEEE.


Hutter, F., Kotthoff, L., and Vanschoren, J., editors (2019). _Automated Machine Learning: Methods, Sys-_
_tems, Challenges_ [. Springer. In press, available at http://automl.org/book.](http://automl.org/book)


31
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _REFERENCES_


Inouye, T., Shinosaki, K., Sakamoto, H., Toi, S., Ukai, S., Iyama, A., Katsuda, Y., and Hirano, M. (1991).
Quantification of EEG irregularity by use of the entropy of the power spectrum. _Electroencephalography_
_and clinical neurophysiology_, 79(3):204–210.


Jalili, M., Barzegaran, E., and Knyazeva, M. G. (2013). Synchronization of EEG: bivariate and multivariate
measures. _IEEE Transactions on Neural Systems and Rehabilitation Engineering_, 22(2):212–221.


James, C. J. and Lowe, D. (2003). Extracting multisource brain activity from a single electromagnetic
channel. _Artificial Intelligence in Medicine_, 28(1):89–104.


Jasper, H. (1958). Report of the committee on methods of clinical examination in electroencephalography.
_Electroencephalogr Clin Neurophysiol_, 10:370–375.


Katz, M. J. (1988). Fractals and the analysis of waveforms. _Computers in biology and medicine_, 18(3):145–
156.


Kemp, B., V¨arri, A., Rosa, A. C., Nielsen, K. D., and Gade, J. (1992). A simple format for exchange of
digitized polygraphic recordings. _Electroencephalography and clinical neurophysiology_, 82(5):391–393.


Kingma, D. P. and Ba, J. (2014). Adam: A method for stochastic optimization. _arXiv preprint_
_[arXiv:1412.6980](http://arxiv.org/abs/1412.6980)_ .


Kiral-Kornek, I., Roy, S., Nurse, E., Mashford, B., Karoly, P., Carroll, T., Payne, D., Saha, S., Baldassano,
S., O’Brien, T., Grayden, D., Cook, M., Freestone, D., and Harrer, S. (2018). Epileptic seizure prediction
using big data and deep learning: Toward a mobile system. _EBioMedicine_, 27:103 – 111.


Krell, M. M., Seeland, A., and Kim, S. K. (2018). Data augmentation for brain-computer interfaces: Analysis
on event-related potentials data. _[arXiv preprint arXiv:1801.02730](http://arxiv.org/abs/1801.02730)_ .


Krizhevsky, A., Sutskever, I., and Hinton, G. E. (2012). Imagenet classification with deep convolutional
neural networks. In _Advances in neural information processing systems_, pages 1097–1105.


Kuhlmann, L., Cook, M., Fuller, K., Grayden, D., Burkitt, A., and Mareels, I. (2008). Correlation analysis
of seizure detection features. In _2008 International Conference on Intelligent Sensors, Sensor Networks_
_and Information Processing_, pages 309–314. IEEE.


Kumar, S. P., Sriraam, N., Benakop, P., and Jinaga, B. (2010). Entropies based detection of epileptic seizures
with artificial neural network classifiers. _Expert Systems with Applications_, 37(4):3284–3291.


Lachaux, J.-P., Rodriguez, E., Martinerie, J., and Varela, F. J. (1999). Measuring phase synchrony in brain
signals. _Human brain mapping_, 8(4):194–208.


Landis, J. R. and Koch, G. G. (1977). The measurement of observer agreement for categorical data. _biomet-_
_rics_, pages 159–174.


Lawhern, V. J., Solon, A. J., Waytowich, N. R., Gordon, S. M., Hung, C. P., and Lance, B. J. (2018).
EEGNet: a compact convolutional neural network for EEG-based brain–computer interfaces. _Journal of_
_neural engineering_, 15(5):056013.


LeCun, Y., Haffner, P., Bottou, L., and Bengio, Y. (1999). Object recognition with gradient-based learning.
In _Shape, contour and grouping in computer vision_, pages 319–345. Springer.


32
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _REFERENCES_


Lehmann, C., Koenig, T., Jelic, V., Prichep, L., John, R. E., Wahlund, L.-O., Dodge, Y., and Dierks, T.
(2007). Application and comparison of classification algorithms for recognition of alzheimer’s disease in
electrical brain activity (eeg). _Journal of neuroscience methods_, 161(2):342–350.


Li, H., Xu, Z., Taylor, G., Studer, C., and Goldstein, T. (2018). Visualizing the loss landscape of neural
nets. In _Advances in Neural Information Processing Systems_, pages 6389–6399.


Lim, S., Kim, I., Kim, T., Kim, C., and Kim, S. (2019). Fast autoaugment. _[arXiv preprint arXiv:1905.00397](http://arxiv.org/abs/1905.00397)_ .


Logesparan, L., Casson, A. J., and Rodriguez-Villegas, E. (2012). Optimal features for online seizure detection. _Medical & biological engineering & computing_, 50(7):659–669.


Lopez de Diego, S. (2017). Automated interpretation of abnormal adult electroencephalography. Master’s
thesis, Temple University.


Loshchilov, I. and Hutter, F. (2016). SGDR: Stochastic gradient descent with warm restarts. _arXiv preprint_

_[arXiv:1608.03983](http://arxiv.org/abs/1608.03983)_ .


Loshchilov, I. and Hutter, F. (2017). Fixing weight decay regularization in Adam. _arXiv preprint_
_[arXiv:1711.05101](http://arxiv.org/abs/1711.05101)_ .


Lotte, F., Bougrain, L., Cichocki, A., Clerc, M., Congedo, M., Rakotomamonjy, A., and Yger, F. (2018). A
review of classification algorithms for EEG-based brain–computer interfaces: a 10 year update. _Journal_
_of neural engineering_, 15(3):031005.


Michel, C. M., Murray, M. M., Lantz, G., Gonzalez, S., Spinelli, L., and de Peralta, R. G. (2004). EEG
source imaging. _Clinical neurophysiology_, 115(10):2195–2222.


Minasyan, G. R., Chatten, J. B., Chatten, M. J., and Harner, R. N. (2010). Patient-specific early seizure
detection from scalp EEG. _Journal of clinical neurophysiology: official publication of the American Elec-_
_troencephalographic Society_, 27(3):163.


Mirowski, P., Madhavan, D., LeCun, Y., and Kuzniecky, R. (2009). Classification of patterns of EEG
synchronization for seizure prediction. _Clinical neurophysiology_, 120(11):1927–1940.


Montavon, G., Samek, W., and M¨uller, K.-R. (2018). Methods for interpreting and understanding deep
neural networks. _Digital Signal Processing_, 73:1–15.


M¨uller-Gerking, J., Pfurtscheller, G., and Flyvbjerg, H. (1999). Designing optimal spatial filters for singletrial EEG classification in a movement task. _Clinical neurophysiology_, 110(5):787–798.


Newton, C. R. and Garcia, H. H. (2012). Epilepsy in poor regions of the world. _The Lancet_, 380(9848):1193–
1201.


Obeid, I. and Picone, J. (2016). The Temple University Hospital EEG data corpus. _Frontiers in neuroscience_,
10, DOI: 10.3389/fnins.2016.00196.


Paszke, A., Gross, S., Chintala, S., Chanan, G., Yang, E., DeVito, Z., Lin, Z., Desmaison, A., Antiga, L.,
and Lerer, A. (2017). Automatic differentiation in PyTorch. In _NIPS-W_ .


Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer,
P., Weiss, R., Dubourg, V., et al. (2011). Scikit-learn: Machine learning in python. _Journal of machine_
_learning research_, 12(Oct):2825–2830.


33
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _REFERENCES_


Peng, C.-K., Havlin, S., Stanley, H. E., and Goldberger, A. L. (1995). Quantification of scaling exponents
and crossover phenomena in nonstationary heartbeat time series. _Chaos: An Interdisciplinary Journal of_
_Nonlinear Science_, 5(1):82–87.


Pereira, A. E., Padden, D., Jantz, J. J., Lin, K., and Alcaide-Aguirre, R. E. (2018). Cross-Subject EEG
Event-Related Potential Classification for Brain-Computer Interfaces Using Residual Networks. working
paper or preprint.


Petrosian, A. (1995). Kolmogorov complexity of finite sequences and recognition of different preictal EEG
patterns. In _Proceedings Eighth IEEE Symposium on Computer-Based Medical Systems_, pages 212–217.
IEEE.


Picone, J. (2019). Comment on inter-rater agreement in the TUH Abnormal EEG Corpus. Personal communication.


Quiroga, R. Q., Blanco, S., Rosso, O., Garcia, H., and Rabinowicz, A. (1997). Searching for hidden information with Gabor Transform in generalized tonic-clonic seizures. _Electroencephalography and clinical_
_Neurophysiology_, 103(4):434–439.


Rajkomar, A., Oren, E., Chen, K., Dai, A. M., Hajaj, N., Hardt, M., Liu, P. J., Liu, X., Marcus, J., Sun, M.,
et al. (2018). Scalable and accurate deep learning with electronic health records. _NPJ Digital Medicine_,
1(1):18.


Ramos-Murguialday, A., Broetz, D., Rea, M., L¨aer, L., Yilmaz, O., Brasil, F. L., Liberati, G., Curado, M. R., [¨]
Garcia-Cossio, E., Vyziotis, A., et al. (2013). Brain–machine interface in chronic stroke rehabilitation: a
controlled study. _Annals of neurology_, 74(1):100–108.


Roberts, S. J., Penny, W., and Rezek, I. (1999). Temporal and spatial complexity measures for electroencephalogram based brain-computer interfacing. _Medical & biological engineering & computing_, 37(1):93–98.


Rose, S. W., Penry, J. K., White, B. G., and Sato, S. (1973). Reliability and validity of visual EEG assessment
in third grade children. _Clinical Electroencephalography_, 4(4):197–205.


Roy, S., Kiral-Kornek, I., and Harrer, S. (2019). ChronoNet: a deep recurrent neural network for abnormal
EEG identification. In _Conference on Artificial Intelligence in Medicine in Europe_, pages 47–56. Springer.


Rumelhart, D. E., Hinton, G. E., Williams, R. J., et al. (1988). Learning representations by back-propagating
errors. _Cognitive modeling_, 5(3):1.


Schapire, R. E. and Freund, Y. (2013). Boosting: Foundations and algorithms. _Kybernetes_ .


Schirrmeister, R. T., Gemein, L., Eggensperger, K., Hutter, F., and Ball, T. (2017a). Deep learning
with convolutional neural networks for decoding and visualization of EEG pathology. _arXiv preprint_
_[arXiv:1708.08012](http://arxiv.org/abs/1708.08012)_ .


Schirrmeister, R. T., Springenberg, J. T., Fiederer, L. D. J., Glasstetter, M., Eggensperger, K., Tangermann,
M., Hutter, F., Burgard, W., and Ball, T. (2017b). Deep learning with convolutional neural networks for
EEG decoding and visualization. _Human brain mapping_, 38(11):5391–5420.


Schr¨oer, S., Killmann, I., Frank, B., Voelker, M., Fiederer, L., Ball, T., and Burgard, W. (2015). An
autonomous robotic assistant for drinking. In _2015 IEEE International Conference on Robotics and Au-_
_tomation (ICRA)_, pages 6482–6487. IEEE.


34
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _A_ _HYPERPARAMETERS_


Sidiropoulos, N. D., De Lathauwer, L., Fu, X., Huang, K., Papalexakis, E. E., and Faloutsos, C. (2017).
Tensor decomposition for signal processing and machine learning. _IEEE Transactions on Signal Processing_,
65(13):3551–3582.


Singh, A. and Trevick, S. (2016). The epidemiology of global epilepsy. _Neurologic clinics_, 34(4):837–847.


Sturm, I., Lapuschkin, S., Samek, W., and M¨uller, K.-R. (2016). Interpretable deep neural networks for
single-trial EEG classification. _Journal of neuroscience methods_, 274:141–145.


Subasi, A. (2007). EEG signal classification using wavelet feature extraction and a mixture of expert model.
_Expert Systems with Applications_, 32(4):1084–1093.


Subasi, A., Kevric, J., and Abdullah Canbaz, M. (2019). Epileptic seizure detection using hybrid machine
learning methods. _Neural Computing and Applications_, 31(1):317–325.


Tangermann, M., Schnorr, N., and Musso, M. (2014). Towards aphasia rehabilitation with bci. In _Proceedings_
_of the 6th International Brain–computer Interface Conference, Graz_, pages 65–68.


Thijs, R. D., Surges, R., O’Brien, T. J., and Sander, J. W. (2019). Epilepsy in adults. _The Lancet_ .


Van Dokkum, L., Ward, T., and Laffont, I. (2015). Brain computer interfaces for neurorehabilitation–its
current status as a rehabilitation strategy post-stroke. _Annals of physical and rehabilitation medicine_,
58(1):3–8.


Van Leeuwen, K., Sun, H., Tabaeizadeh, M., Struck, A., Van Putten, M., and Westover, M. (2019). Detecting
abnormal electroencephalograms using deep convolutional networks. _Clinical neurophysiology_, 130(1):77–
84.


van Putten, M. J., Kind, T., Visser, F., and Lagerburg, V. (2005). Detecting temporal lobe seizures from
scalp EEG recordings: a comparison of various features. _Clinical neurophysiology_, 116(10):2480–2489.


Watter, M. (2014). Epileptic seizure detection with reservoir computing. Master’s thesis, Albert Ludwig
University Freiburg.


Wold, S., Esbensen, K., and Geladi, P. (1987). Principal component analysis. _Chemometrics and intelligent_
_laboratory systems_, 2(1-3):37–52.


World Health Organization, W. (1992). _The ICD-10 classification of mental and behavioural disorders:_
_clinical descriptions and diagnostic guidelines_ . Geneva: World Health Organization.


World Health Organization, W. (2019). Epilepsy: a public health imperative: summary. Technical report,
World Health Organization.

### **A Hyperparameters**


In this section, we report all the hyperparameters used for all the investigated models in our experiments to
allow maximal reproducibility.


35
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _B_ _PERFORMANCE DIFFERENCES TO OLDER EXPERIMENTS_





criterion entropy
bootstrap False
ma ~~x f~~ eatures _√F_



ma ~~x f~~ eatures _F_


mi ~~n s~~ ampels ~~l~~ eaf 2
mi ~~n s~~ amples ~~s~~ plit 2
ma ~~x d~~ epth 90
~~n e~~ stimators 1600

|RF|SVM|Riemannian (SVM)|SVM (on covariance matrices)|
|---|---|---|---|
||100<br>1_/_<br>_√_<br>_F_|10<br>1_/_(_E ∗_(_E_ + 1)_/_2)|1000<br>1_/_(_E ∗_(_E_ + 1)_/_2)|
|entropy<br>False<br>_√_<br>_F_<br>2<br>2<br>90<br>1600||||



Total run time limit 12h

Per run time limit 4h



Table S1: Hyperparameters of feature-based approaches. Optimized using CV.


Hyperparameter BD-Deep4 BD-Shallow BD-TCN BD-EEGNet
batc ~~h s~~ ize 64 64 64 64

ma ~~x e~~ pochs 35 35 35 35
~~n s~~ tar ~~t c~~ hans 25 40

~~n c~~ hans 21 21 21 21

fina ~~l c~~ on ~~v l~~ ength 1 25 18
~~n c~~ ha ~~n f~~ actor 2

mode ~~l c~~ onstraint None None None None

ini ~~t l~~ r 0.01 0.000625 0.0011261049710243193 0.001

weigh ~~t d~~ ecay 0.0005 0 5.83730537673086e-07 0
l2 decay 1.7491630095065614e-08
inpu ~~t t~~ ime ~~l~~ ength 6000 6000 6000 6000
strid ~~e b~~ efor ~~e p~~ ool True
dropout 0.5 0.5 0.05270154233150525 0.25


Table S2: Hyperparameters of neural netowkrs. Optimized in previous experiments (default values were
used for BD-EEGNet).

### **B Performance differences to older experiments**


We determined marginally different results for our BD-Deep4 and BD-Shallow decoding pathology compared
to older experiments. In our previous publication Schirrmeister et al. (2017a), we reported a final decoding
accuracy of 85.4% using BD-Deep4 (here 84.57%) and 84.5% using BD-Shallow (here 84.13%). We assume
that the differences are due to the other optimizations used in training the networks. Where we previously
used max-norm constraint, no weight decay, optimizer Adam, and a fixed learning rate, we now used cosine
annealing to schedule learning rate and weight decay, and used optimizer AdamW. In certain experiments, we
observed updates in the last epochs that decreased the classification accuracy. It could be possible that with
this updated optimization, other hyperparameters must be adjusted to yield even more robust and superior
results. Furthermore, the data set has been updated. The current version is TUH Abnormal EEG Corpus
(v2.0.0); in our previous publication, we used version (v1.1.1). The updates included removing duplicates
that were present in both training and final evaluation sets, which possibly made the classifications of these


36
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _D_ _RIEMANNIAN-GEOMETRY-BASED DECODING_


recordings easier.

### **C Neural network parameters**


In Table S3 we display the number of parameters of each investigated neural network architecture. They
were computed by summation of the sizes of layers as returned by PyTorch [18] [Paszke et al. (2017)]. The
complexity of models from low to high is BD-EEGNet, BD-Shallow, BD-Deep4,and BD-TCN. In our analysis,
models with more parameters achieved higher accuracies.


Model Parameters [ _×_ 10 [3] ] Receptive field
BD-TCN 457 903

BD-Deep4 277 600
BD-Shallow 37 608

BD-EEGNet 7 597


Table S3: Investigated neural network architectures and related number of parameters and receptive field
sizes. BD-TCN is most complex and has largest receptive field, BD-EEGNet is, significantly, the simplest
model.

### **D Riemannian-geometry-based decoding**


We investigated the influence of averaging covariance matrices for Riemannian-geometry-based decoding using Euclidean and geometric mean, and tangent space mapping [Figure S4]. As could be expected [Barachant


**Mean** **Subset** **Tangent Space** **Accuracy** **[%]**
Euclidean Cross-Validation False 73.64

True 80.00

Final evaluation False 76.81

True 84.42

Geometric Cross-validation False 78.57

True 81.26

Final evaluation False 81.52

True 85.87


Table S4: Comparison of Riemannian-geometry-based decoding using arithmetic mean, geometric mean, and
optional tangent space mapping. Using tangent space mapping and geometric mean estimation yielded best
performance.


et al. (2013)], aggregation with the geometric mean yields superior decoding accuracies. Additionally, tangent
space mapping yielded substantial improvements.


18 available for download at `[https://pytorch.org/get-started/locally/](https://pytorch.org/get-started/locally/)`


37
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _E_ _THREE MODEL ENSEMBLES ERRORS_

### **E Three model ensembles errors**


In Table S5, we display the analysis of the errors of the three-tuples of the models for ensembling. We chose
those three models (BD-Deep4, RF, RG) that indicated the highest ratio (44,56%) of CV label errors made
by exactly one of the models, as these could be reduced by majority voting.


38
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


_Lukas A. W. Gemein_ _E_ _THREE MODEL ENSEMBLES ERRORS_


Model 1 Model 2 Model 3 E0 E1 E2 E3 E1 Ratio [%]


0 BD-Deep4 BD-Shallow BD-TCN 2163 166 110 277 30.02
1 BD-Deep4 BD-Shallow BD-EEGNet 2130 177 123 286 30.20
2 BD-Deep4 BD-Shallow RF 2084 240 127 265 37.97
3 BD-Deep4 BD-Shallow SVM 2053 255 149 259 38.46
4 BD-Deep4 BD-Shallow RG 2006 299 193 218 42.11
5 BD-Deep4 BD-TCN BD-EEGNet 2158 150 121 287 26.88
6 BD-Deep4 BD-TCN RF 2108 218 127 263 35.86
7 BD-Deep4 BD-TCN SVM 2084 227 140 265 35.92
8 BD-Deep4 BD-TCN RG 2021 304 166 225 43.74
9 BD-Deep4 BD-EEGNet RF 2092 201 145 278 32.21
10 BD-Deep4 BD-EEGNet SVM 2056 238 138 284 36.06
11 BD-Deep4 BD-EEGNet RG 1990 312 179 235 42.98
12 BD-Deep4 RF SVM 2039 241 175 261 35.60
**13** **BD-Deep4** **RF** **RG** **1962** **336** **207** **211** **44.56**
14 BD-Deep4 SVM RG 1953 322 221 220 42.20
15 BD-Shallow BD-TCN BD-EEGNet 2144 178 107 287 31.12

16 BD-Shallow BD-TCN RF 2111 216 122 267 35.70

17 BD-Shallow BD-TCN SVM 2056 272 134 254 41.21

18 BD-Shallow BD-TCN RG 2033 286 166 231 41.87

19 BD-Shallow BD-EEGNet RF 2077 227 138 274 35.52

20 BD-Shallow BD-EEGNet SVM 2024 269 172 251 38.87

21 BD-Shallow BD-EEGNet RG 1993 295 204 224 40.80

22 BD-Shallow RF SVM 2012 278 182 244 39.49

23 BD-Shallow RF RG 1970 325 205 216 43.57

24 BD-Shallow SVM RG 1935 343 233 205 43.92

25 BD-TCN BD-EEGNet RF 2108 195 137 276 32.07

26 BD-TCN BD-EEGNet SVM 2059 240 153 264 36.53

27 BD-TCN BD-EEGNet RG 2010 305 161 240 43.20

28 BD-TCN RF SVM 2049 236 183 248 35.38

29 BD-TCN RF RG 1992 313 191 220 43.23

30 BD-TCN SVM RG 1962 331 204 219 43.90

31 BD-EEGNet RF SVM 2018 253 178 267 36.25

32 BD-EEGNet RF RG 1960 321 207 228 42.46

33 BD-EEGNet SVM RG 1925 346 221 224 43.74

34 RF SVM RG 1924 337 234 221 42.55


Table S5: Overview of all investigated ensembles of three models indicating number of label errors made
by none of the models (E0), by exactly one (E1), by two (E2) or by all of the models (E3) and indicating
ratio of E1 errors that could potentially be reduced by combining three models in an ensemble. Highlighted
models were chosen for ensembling.


39
_⃝_ c 2019. Licensed under the CC-BY-NC-ND license `creativecommons.org/licenses/by-nc-nd/4.0/` .


