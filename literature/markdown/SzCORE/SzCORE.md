# **SzCORE: A Seizure Community Open-source** **Research Evaluation framework for the validation** **of EEG-based automated seizure detection** **algorithms**

Jonathan Dan [1*] Una Pale [1] Alireza Amirshahi [1] William Cappelletti [2]


Thorir Mar Ingolfsson [3] Xiaying Wang [3] Andrea Cossettini [3] Adriano Bernini [4]


Luca Benini [3,5] Sándo Beniczky [6] David Atienza [1] Philippe Ryvlin [4]


**1** Embedded Systems Laboratory, EPFL, Switzerland
**2** LTS4, EPFL, Switzerland
**3** Integrated Systems Laboratory, ETH Zürich, Switzerland
**4** Service of neurology, Centre Hospitalier Universitaire Vaudois, Switzerland
**5** Department of Electrical, Electronic and Information Engineering (DEI), University of Bologna, Italy
**6** Aarhus University Hospital and Danish Epilepsy Centre, Aarhus University, Dianalund, Denmark


March 11, 2024


**Abstract**


_The need for high-quality automated seizure detection algorithms based on electroencephalography (EEG) becomes ever more_
_pressing with the increasing use of ambulatory and long-term EEG monitoring. Heterogeneity in validation methods of_
_these algorithms influences the reported results and makes comprehensive evaluation and comparison challenging. This_
_heterogeneity concerns in particular the choice of datasets, evaluation methodologies, and performance metrics. In this_
_paper, we propose a unified framework designed to establish standardization in the validation of EEG-based seizure detection_
_algorithms. Based on existing guidelines and recommendations, the framework introduces a set of recommendations and_
_standards related to datasets, file formats, EEG data input content, seizure annotation input and output, cross-validation_
_strategies, and performance metrics. We also propose the 10-20 seizure detection benchmark, a machine-learning benchmark_
_based on public datasets converted to a standardized format. This benchmark defines the machine-learning task as well as_
_reporting metrics. We illustrate the use of the benchmark by evaluating a set of existing seizure detection algorithms. The_
_SzCORE (Seizure Community Open-source Research Evaluation) framework and benchmark are made publicly available_
_along with an open-source software library to facilitate research use, while enabling rigorous evaluation of the clinical_
_significance of the algorithms, fostering a collective effort to more optimally detect seizures to improve the lives of people_
_with epilepsy._


**Foreword** _This pre-print version of the manuscript intends to collect contributions from the community in order to_
_propose a unified methodology for the validation of seizure detection algorithms in people with epilepsy._
_We invite the community to comment on the proposed framework by filling in the following form:_ _`[https: // forms. gle/](https://forms.gle/XfbDaJQi2VooWRN2A)`_
```
   XfbDaJQi2VooWRN2A

```

#### **1 Introduction**

Scalp EEG-based seizure detection algorithms can
optimize and facilitate the diagnostic workup performed in people with epilepsy (PWE) to improve
patients’ care and quality of life [1]. Currently, such
algorithms are primarily used during in-hospital
long-term video-EEG monitoring (LTM) performed
in epilepsy monitoring unit (EMU) over periods of
a few days to several weeks. Recordings can be processed on line (i.e. in real time) or off line. Realtime detection helps inform the EMU staff about


- [Corresponding author: jonathan.dan@epfl.ch](mailto:jonathan.dan@epfl.ch)



an ongoing seizure, thus promoting prompt intervention [2], while off-line detection can reduce the
physician’s EEG reading workload and help detect
subtle seizures.


In the last decade, home-based video-EEG has been
gradually developed as an alternative to EMU LTM,
which enables the prospect of very long-term ambulatory EEG [3]. Home-based video-EEG has similar
diagnostic objectives to EMU LTM but can last longer,
thanks to lower daily cost and patient and healthcare
system burden [4]. It also benefits from automatic
seizure detection since it is performed without the
permanent supervision of healthcare professionals,


### Framework Benchmark
##### SzCORE 10-20 seizure detection








|Framewo SzCORE|Data format ork|
|---|---|
||Data format|
|dataset<br>...<br>sub-01<br>sub-01_rec-01.edf<br>sub-01_rec-01.tsv<br>EDF<br>• 256 Hz<br>• unipolar<br>• 10-20 electrodes<br>TSV<br>• start, duration<br>• SCORE sz types<br>• channels<br>|dataset<br>...<br>sub-01<br>sub-01_rec-01.edf<br>sub-01_rec-01.tsv<br>EDF<br>• 256 Hz<br>• unipolar<br>• 10-20 electrodes<br>TSV<br>• start, duration<br>• SCORE sz types<br>• channels<br>|


|Col1|Datasets|Col3|
|---|---|---|
|CHB-MIT Scalp EEG<br>TUH EEG Sz Corpus<br>Sienna Scalp EEG<br>SeizeIT1<br>23<br>675<br>14<br>42<br>198<br>4029<br>47<br>182<br>982 h<br>1476 h<br>128 h<br>4211 h|CHB-MIT Scalp EEG<br>TUH EEG Sz Corpus<br>Sienna Scalp EEG<br>SeizeIT1<br>23<br>675<br>14<br>42<br>198<br>4029<br>47<br>182<br>982 h<br>1476 h<br>128 h<br>4211 h|CHB-MIT Scalp EEG<br>TUH EEG Sz Corpus<br>Sienna Scalp EEG<br>SeizeIT1<br>23<br>675<br>14<br>42<br>198<br>4029<br>47<br>182<br>982 h<br>1476 h<br>128 h<br>4211 h|














|Col1|Evaluation methodology|
|---|---|
|Subject-independent models<br> _leave subjects out_<br>Personalized models<br> _time series cross-validation_<br>training data<br>test data<br>split 1<br>split 2<br>split n<br>...|Subject-independent models<br> _leave subjects out_<br>Personalized models<br> _time series cross-validation_<br>training data<br>test data<br>split 1<br>split 2<br>split n<br>...|


|Col1|ML task|Col3|
|---|---|---|
|Personalized<br>Subject-independent<br>    on a single dataset<br>Subject-independent<br>           across datasets<br>Input Data<br>10-20 scalp EEG<br>Segment seizures<br>onset, duration<br>Output<br>Task<br>Models|||

















|Col1|Performance metrics|
|---|---|
|Sample-based scoring<br>Event-based scoring<br>Reference<br>Hypothesis<br>True Positives<br>False Negatives<br>False Positives<br>0<br>0<br>0<br>0<br>0<br>0<br>0<br>1<br>1<br>1<br>1<br>1<br>1<br>1<br>1<br>1<br>1<br>0<br>1<br>1<br>1<br>1<br>0<br>0<br>1<br>1<br>1<br>1<br>1<br>1<br>1<br>0<br>1<br>1<br>Reference<br>Hypothesis|Sample-based scoring<br>Event-based scoring<br>Reference<br>Hypothesis<br>True Positives<br>False Negatives<br>False Positives<br>0<br>0<br>0<br>0<br>0<br>0<br>0<br>1<br>1<br>1<br>1<br>1<br>1<br>1<br>1<br>1<br>1<br>0<br>1<br>1<br>1<br>1<br>0<br>0<br>1<br>1<br>1<br>1<br>1<br>1<br>1<br>0<br>1<br>1<br>Reference<br>Hypothesis|


|Col1|Reporting|Col3|
|---|---|---|
||||
|• Sensitivity<br>• Precision<br>• F1-score<br>• False alarms / day<br>• Model details<br>• Software doc<br>• Data<br>• Results & Metrics<br><br>Sample & Event<br>Metrics<br>Model Card|||


_Graphical abstract_



**2**


and generates large volumes of data.
Ultra long-term ambulatory monitoring has a different scope from LTM and home-based video-EEG
recording [5, 6, 7]. It can be used to inform PWE and
their caregivers of an ongoing seizure to enable protective interventions, provide physicians with more
precise seizure counts than that recalled by PWE
and their caregivers to optimize therapy, and document eventual recurrence patterns, which may allow
seizure forecasting [8].
The field of EEG-based seizure detection has benefited from advances in machine learning and the
provision of EEG datasets from PWE to train such
models. Yet, such datasets with annotated seizures
remain rare and often kept private as they must comply with strict legal requirements for personal health
data. In contrast, open-source datasets are recognized as catalysts for developing machine-learning
algorithms [9]. The machine-learning task can be
formulated as a segmentation problem that aims at
identifying the start and end of each seizure event.
However, current automated scalp EEG-based seizure
detection solutions do not meet the level of performance of human experts [10].
A key obstacle hindering progress in the field is the
lack of standardized protocols for the training and
evaluation of seizure detection algorithms. When
developing a novel algorithm, researchers can opt
to re-implement selected algorithms for comparison
within their own evaluation framework. Such a process is highly time-consuming. Therefore, it is rarely
done in practice, resulting in analyses relying on
reported metrics that are not necessarily comparable [1]. This issue has been tackled in other research
fields by providing a standard machine-learning task
definition and benchmark, effectively leading to dramatic improvements in fields such as image classification [11], conversational agents [12] or computational
models of brain function [13].
The validation of seizure detection algorithms lacks
standardization in EEG datasets, evaluation methodology and performance metrics, as discussed in detail
below.


**EEG datasets** collected for the purpose of individual studies are common in the field [1, 14, 15]. Such
private datasets prohibit direct comparison with studies on other datasets, as algorithm performance is
highly data-dependent [16]. To date, several datasets
have been made publicly available, including Physionet CHB-MIT Scalp EEG Database [17, 18], TUH
EEG Seizure Corpus [19], Physionet Siena Scalp EEG
Database [20, 21, 18], and SeizeIT1 [22]. Working
with multiple datasets is challenging owing to various data formats, e.g. disparities in EEG electrodes,
reference electrodes, montage, channel nomencla


ture, channel sequence, sampling frequencies, and
annotation formats. A previous community effort
attempted to standardize EEG for computer-based
assessment and reporting of EEG, suggesting the
SCORE nomenclature, which has been endorsed by
the International League Against Epilepsy (ILAE)
and International Federation of Clinical Neurophysiology (IFCN) [23]. Others have worked on a unified
organization of brain imaging files and metadata,
suggesting the Brain Imaging Data Structure (BIDS),
which is increasingly used in research [24] and which
was then extended to organize EEG data [25]. Recent
work has made SCORE machine readable and com
patible with BIDS through the HED-SCORE schema
specification [26]. In subsection 2.1 of our framework,
_we propose a standard data format for storing EEG and_
_associated seizure annotations that is based on the BIDS-_

_EEG standard and the HED-SCORE nomenclature. The_

_data format provides standardized inputs and outputs for_
_seizure detection algorithms, allowing any seizure detec-_
_tion algorithm to be operated on any thus standardized_
_dataset. Furthermore, this allows visualization and pro-_
_cessing of output seizure annotations irrespective of the_
_algorithm that produces them._


**Evaluation methodology** has a large influence on
reported results. Cross-validation is a statistical
method used in machine learning to estimate the
performance of an algorithm on an independent
dataset [27]. To perform cross-validation, the data
are split into two sets: a training set and a test set [1] .
The performance of an algorithm is reported as the
average performance on all test sets after generating
multiple models using different splits of training and
test data. Many methods exist to split the data, but
they do not necessarily meet the requirement of independence between the training and test sets, which
could lead to overestimation of the performance of an
algorithm. Overestimation of the accuracy of patientindependent models can occur if some of the same
subjects are present in both the training and test sets
or when datasets are too small [28]. Moreover, the
chronology of recordings should be respected by only
using data in the training set that was acquired prior
to the acquisition of the data in the test set for personalized models [29]. In subsection 2.2, _we propose rec-_
_ommendations for cross-validation of subject-independent_
_and personalized models_ .


**Performance metrics** are critical to estimate the performance of automatic seizure detection. The cur
rent use of different metrics makes it difficult to
perform comparisons between studies. Reported results use different combinations of general perfor

1 In this paper, we do not cover the notion of a validation set that
can be used to determine hyperparameters of a model.


**3**


mance metrics, such as sensitivity, specificity, precision, accuracy, area under the receiver operating
characteristic curve, f1-score, false-alarm rate, etc.
These metrics are computed by comparing groundtruth reference annotations provided by a human
expert with hypothesis annotations provided by an
algorithm. This comparison allows counting of “true
positives” (TP; i.e. seizures correctly detected by
the algorithm), “false positives” (FP; i.e. incorrectly
labeled as seizures by the algorithm), and “false negatives” (FN; i.e. seizures missed by the algorithm).


However, TP, FP, and FN can be counted using either _sample-based_ scoring or _event-based_ scoring, which
can result in very different interpretations of the performance metrics. Sample-based scoring computes
performance metrics on a sample-by-sample basis
and is sometimes referred to as epoch-based scoring [30] or window-based scoring. Sample-based
scoring is widely adopted by the machine-learning
community and it integrates tightly with standard
training schemes. While sample-based scoring captures the fine detail agreement between the reference
and hypothesis annotations at the time-scale of labels,
it does not provide answers to the clinically relevant
questions: _"How many seizures did the patient have?"_ or
_"How many seizures were missed by the seizure detection_
_algorithm?"_ or _"How many false alarms were triggered by_
_the system?"_ . Answering these questions requires a
scoring method that operates at the granularity level
of events (or epileptic seizures), i.e. event-based scoring. This can be computed in many different ways,
such as ’Any-overlap’ (OVLP) or ’Time-aligned event
scoring’ (TAES) [30]. _In subsection 2.3, we propose met-_
_rics for the evaluation of seizure detection algorithms that_
_are designed to address questions of the clinical community_
_and requirements of the machine-learning community_ .


In summary, the lack of common research practices
regarding datasets, cross-validation methodologies
and performance metrics when validating seizure detection algorithms is a limiting factor for sound evaluation of algorithms. In this paper, _we propose an open_
_framework for the validation of EEG-based seizure detec-_
_tion algorithms: SzCORE_ . This framework is the result
of discussions with stakeholders in the field, including PWE, physicians and other healthcare providers,
engineers, computer scientists, and other scientists
working on the development of seizure detection algorithms. It aims to lift the technical barriers that
slow down the development of new algorithms, allowing them to operate on multiple datasets and
to be assessed using a fair and objective methodology. Based on the framework, we propose the _10-_
_20 EEG seizure detection benchmark_ (Section 3) that
defines the datasets, tasks and performance evaluation of seizure detection algorithms. Addition

**4**



ally, we provide an open-source code library available on GitHub: `[https://github.com/esl-epfl/](https://github.com/esl-epfl/sz-validation-framework)`
`[sz-validation-framework](https://github.com/esl-epfl/sz-validation-framework)` . The library is designed
to allow continuous improvement by the community.
The framework, benchmark and supporting code library are described on an online platform: `[https://](https://eslweb.epfl.ch/epilepsybenchmarks)`
`[eslweb.epfl.ch/epilepsybenchmarks](https://eslweb.epfl.ch/epilepsybenchmarks)`, which also
serves as the central hub for a community-built
benchmark, where new seizure detection algorithms
can be fairly compared.

#### **2 SzCORE framework**


**2.1 EEG Datasets and data format**


**Datasets** Datasets should include EEG raw signals,
recording specifics, seizure annotations, and patient
details, e.g. according to BIDS-EEG specifications [24,
25]. They should be organized to allow computer
systems to process them efficiently. An example
of BIDS-EEG data file-structure organization for a
dataset of PWE is provided in Appendix A.1.


**EEG data format:** To allow algorithms to operate
seamlessly on any dataset, we propose standardization of EEG data that is at least consistent with

the IFCN and ILAE minimum recording standards
that are recommended for EEG [31]. Recordings
should be stored in `.edf` files. They should contain
the 19 electrodes of the international 10-20 system
in a unipolar common average montage. The
recording should be resampled to 256 Hz for
storage, and original data should be acquired with
a sampling frequency of at least 256 Hz. The
channels should be provided in the following order: `Fp1-Avg, F3-Avg, C3-Avg, P3-Avg, O1-Avg,`
```
F7-Avg, T3-Avg, T5-Avg, Fz-Avg, Cz-Avg,
Pz-Avg, Fp2-Avg, F4-Avg, C4-Avg, P4-Avg,
```

`O2-Avg, F8-Avg, T4-Avg, T6-Avg` . Additional
data channels can optionally be provided after these
19 channels; they should not be used to compute the

common average.


**Seizure annotation format:** The annotation format

should be constructed in a way that it can be used
both for original annotations (ground truth) and the
output of seizure detection algorithms. The format
we propose is a tab-separated values ( `.tsv` ) file that
is human-readable. It is a text file that uses a tab
as a delimiter to separate the different columns of
information, with each row representing one event.
Each annotation file is associated with a single EEG
recording. A detailed description and an example
of the information contained in annotation files is
provided in appendix A.2. These files adhere to
the BIDS-EEG guidelines and use the hierarchical


ILAE-based classification of seizures defined by HEDSCORE [24, 32, 26]. The seizure nomenclature is
presented in Figure 4 in Appendix A.2.


**2.2 Evaluation methodology**


To evaluate seizure detection algorithms, a training
set is used to determine the parameters of the machine learning algorithm and an independent test set
is used to estimate the performance of the algorithm.
These sets should be independent to guarantee that
results can be generalized to other data. If data are
only available from a single setting, the dataset can
be split into a training set and a test set. This process is repeated multiple times (i.e. folds) to obtain
robust estimates of performance by rotating data
between the training set and the test set, i.e. crossvalidation [27].


**Personalized models** are trained for a specific patient. These models should successfully detect
seizures in unknown recording sessions that took
place after the model was initially trained. _To evaluate_
_these models, at each fold, the training set should only_
_include data that was acquired prior to the acquisition_
_of the test set;_ this is referred to as time-series-crossvalidation (TSCV).
TSCV can be performed in two ways:


 - Training data increase as the model is evaluated
on future test folds (variable amount of data, Fig.
1a).

 - Training data keeps a fixed size with past folds
removed from the training data as the model is
evaluated on future folds (fixed amount of data,
Fig. 1b).


**Subject-independent models** are designed to operate on data from any patient and seizure type. These
models should successfully detect seizures in subjects
whose data were not used to train the model.

Several methods can be used to validate subjectindependent models, provided that independence of
subjects between training and test sets is maintained.:


 - _Leave-one-subject-out (LOO)_ is a technique in
which many different models are trained [33].
Each model is trained using all the data except
those from one subject. The data from that subject is used for testing. This allows maximization
of the amount of training data provided to the
model. Final performance is reported by averaging the testing results of all subjects (each using
their subject-independent model). This strategy
also allows assessment of the performance of
each subject, which can then be compared between different algorithms. However, the technique is not appropriate for large datasets with



many subjects, as training models can be computationally expensive and need to be retrained
for every subject.

 - _K-fold cross-validation_ uses a similar strategy to
LOO [33]. The dataset is split into a training
and testing subset with a ratio of subjects of
( _K_ _−_ 1 ) / _K_ for the training set and 1 / _K_ for the
test set. This split is repeated _K_ times until all
subjects are included once in the test set. For
each split, a model is trained and performance
is reported as an average of each model. This is
faster to train and test and, thus, more appropriate for larger datasets as the number of splits is
determined by _K_, irrespective of the number of
subjects. However, this method uses less data
in the training set than LOO, which can lead
to sub-optimal models with larger variability in
estimated performance. LOO is a special case
of K-fold, where _K_ is equal to the number of
subjects.

 - _Fixed training and test sets_ with predetermined
subjects in each set are appropriate for large
datasets (e.g. TUH EEG Sz Corpus). However, it
can lead to more variability in estimated performance in small datasets.


While cross-validation allows a fair assessment of

algorithms during development, the performance of
algorithms for real-world use should be evaluated
on large independent datasets which are currently
missing in our community.


**2.3 Performance metrics**


To assess the performance of seizure detection algorithms, we propose two complementary scoring methodologies, sample-based and event-based
scoring. Both these scoring metrics should be reported when communicating results of algorithms
as sampled-based metrics provide a high granularity
to machine-learning experts and event-based metrics
provide clinically relevant results.


**Sample-based scoring** compares annotation labels,
which are provided at a fixed frequency (we propose
1 Hz), sample by sample to detect TP, FP and FN,
as shown in figure 2. We propose a frequency of
labels of 1 Hz, as it corresponds to the resolution expected by a human annotator. It should be noted, this
frequency does not dictate the duration of data windows used to generate machine-learning predictions.
These can use an arbitrary duration and overlap as
long as they provide predictions at 1 Hz. For annotation labels that overlap only partially with epileptic
seizures, we propose to assign a “seizure” label to a
sample if the overlap exceeds 50%.


**5**


![](/mnt/c/Users/JJ/Desktop/Clarity-Digital-Twin/SeizureTransformer/literature/markdown/SzCORE/SzCORE.pdf-5-0.png)

**Figure 1:** _Time series cross-validation for personalized models. Each box represents an epoch of data. Orange boxes are used for_
_training, purple boxes are used for testing. Each row represents a cross-validation fold. The final results are calculated by appending all_
_cross-validation folds (shown in the last row). a) cross-validation scheme with variable amount of data. b) cross-validation scheme with_
_fixed amount of data._


Another issue concerns seizure duration. As most

seizures do not occur in rapid succession, it is reasonable to merge annotations separated by only a
few seconds. Finally, because seizures are only exceptionally longer than five minutes (longer events are
defined as a status epilepticus [36]) long events are
split into multiple events of a maximum of 5 minutes.
These considerations are encoded into the follow
ing additional rules and parameters to count seizures:



![](/mnt/c/Users/JJ/Desktop/Clarity-Digital-Twin/SeizureTransformer/literature/markdown/SzCORE/SzCORE.pdf-5-3.png)

**Figure 2:** _Sample-based scoring compares annotation labels_
_sample by sample. Correct detections (True Positives), false_
_detections (False Positives), missed detections (False Negatives)._
_Seizure annotations are indicated in purple._


**Event-based scoring** in which events are seizures,
relies on overlap between reference and hypothesis
annotations (Figure 3). Overlap is considered as correct detection, i.e. TP. If the hypothesis event does
not overlap with a reference event, it is counted as
FP.

Accurate annotations of epileptic seizures marking
a clear start and end is notoriously difficult. This
may be complicated by gradual changes in EEG at
the beginning and end of seizures or by other factors, e.g. muscle or movement artifacts. Subtle EEG
changes prior to the marked seizure onset or following marked offset are often detected by various algorithms [34, 35]. Some tolerance is therefore required
with regard to the start and stop time of seizure
to match annotations between two reviewers (e.g.
computer algorithm and human expert). From a
practical perspective, many applications of seizure
detection algorithms should not be negatively impacted if the algorithm marks seizures slightly earlier
or a bit longer than ground-truth annotations. On
the contrary, early detection could be beneficial to
the patient when the detection algorithm serves as
an alarm.


**6**



**Minimum overlap** Minimum overlap between the
reference and hypothesis for a detection. We use
any overlap, however short, to enhance sensitivity.
**Pre-ictal tolerance** Tolerance with respect to the start
time of an event that would count as a detection.

We advise a 30 seconds pre-ictal tolerance.
**Post-ictal tolerance** Tolerance with respect to the
end time of an event that would still count as

a detection. We advise a 60 seconds post-ictal
tolerance.

**Minimum duration between events** Automatically
merge events that are separated by less than
the given duration. We advise merging events
separated by less than 90 seconds which
corresponds to the combined pre and post-ictal
tolerance.

**Maximum event duration** Split events longer than
a given duration into multiple events. We advise
splitting events longer than 5 minutes.


**Performance metrics:** Both the sample-based scoring and event-based scoring produce a count of
correct detections (TP), missed detections (FN) and
wrong detections (FP). These can be used to compute common performance metrics, as defined below.
Specifically, sensitivity and precision are of high interest. F1-score is used as a combined measure con
taining information on both sensitivity and precision.


![](/mnt/c/Users/JJ/Desktop/Clarity-Digital-Twin/SeizureTransformer/literature/markdown/SzCORE/SzCORE.pdf-6-2.png)

**Figure 3:** _Event-based scoring is based on overlap. It defines a_
_set of rules for event merging, tolerance before and after events,_
_and maximum event duration. Correct detections (True Posi-_
_tives), false detections (False Positives). Seizure annotations are_
_indicated in purple_


**Sensitivity** Percentage of reference seizures detected
by the hypothesis. Computed as: _TP_ / ( _TP_ +
_FN_ )
**Precision** Percentage of correct detections over all
hypothesis events. Computed as: _TP_ / ( _TP_ + _FP_ )
**F1-score** Harmonic mean of sensitivity and
recall. Computed as: 2 _∗_ _sensitivity_ _∗_
_precision_ / ( _sensitivity_ + _precision_ )
**False alarms per day** Number of falsely predicted
(FP) seizure events, averaged or interpolated to
number per day.


We explicitly _avoid using metrics that rely on a count_
_of TN, such as specificity and accuracy. This is because_
_in the context of event-based scoring, non-seizure events_
_are ill-defined, and in the context of sample-based scoring,_
_non-seizure samples are much more numerous than seizure_
_samples given the rarity of seizures, resulting in extremely_
_high scores for specificity and accuracy, with little clinical_
_relevance._ Errors of the algorithms

#### **3 Benchmark**


The framework described above allows to build a

standard by which seizure detection algorithms can
be compared. Here, we propose a _10-20 seizure detec-_
_tion benchmark_ . That defines:


 - The data that should be used when evaluating
algorithms.

 - The task and different scenarios that the algorithms should analyze.

 - The performance metrics and reporting guidelines for these algorithms.


**3.1 Benchmark datasets**


Datasets should be publicly and freely available to allow reproducibility testing. Currently, four large public datasets are available [37, 22], namely Physionet
CHB-MIT Scalp EEG Database, TUH EEG Seizure



Corpus, Physionet Siena Scalp EEG, and SeizIT1. A
summary of the data contained in these datasets is
provided in Table 1.
The currently available public EEG datasets do not
all meet the minimum recording requirements of the
framework. To use them, the following manipulations are required:


 - EEG signals are resampled to 256 Hz.

 - Channels are renamed and rereferenced to 10-20

EEG with a common average reference.

 - Annotations are converted to BIDS-EEG/HEDSCORE compliant `.tsv` files.

 - Data are reorganized according to BIDS-EEG
specifications.

 - Some recordings of the TUH EEG Seizure corpus
do not contain all 19 electrodes from the 10-20

system. Missing electrodes are replaced by zero
values.


An exception is the Physionet CHB-MIT Scalp EEG
Database which provides only bipolar channels for
which a conversion to the proposed unipolar montage is not possible. This dataset is analyzed with the
original bipolar montage.


**3.2 Machine-learning task**


The machine-learning task can be formulated as a
segmentation problem that aims at identifying the
start and end of each seizure event. Three test sce
narios are proposed for the evaluation of seizure
detection algorithms:


1. Personalized models

2. Subject-independent models evaluated on a single dataset
3. Subject-independent models evaluated across
datasets


**Personalized models** require sufficient data per subject in terms of number of seizures ( _≥_ 3) [2] and duration ( _≥_ 1 _h_ 30) [3] to be effectively trained and evaluated. For this reason, only the following datasets are
considered: CHB-MIT, Siena, SeizeIT [4] . TSCV with a
variable amount of data is used. The initial training
set includes at least five hours and a minimum of one
seizure. Performance is evaluated on the following
hour. The process is repeated by successively adding
one hour of training data and testing on the next
hour until the end of the recording. Performance
per subject is calculated for sample and event-based


2 Three seizures allow at least one seizure for training, validation
and test set.
3 Two hours correspond to 30min of data around each seizure.
4 TUH Seizure dataset is excluded as it does not contain enough
data (10 minutes on average) per subject and less than three
seizures per subject.


**7**


**Table 1:** _Publicly available scalp EEG datasets of people with epilepsy._


Overview Recordings Data
Dataset `#` subjects duration `#` seizures `#` files avg. duration fs [Hz] `#` channels


CHB-MIT 23 982 h 198 686 60 min 256 22–38

TUH 675 1476 h 4029 7377 10 min [250–1000] 17–128
Siena 14 128 h 47 41 150 min 512 35–45

SeizeIT1 42 4211 h 182 458 612 min 250 26



metrics by aggregating all one-hour test sets. The
performance of a dataset is computed as the average
performance of individual subjects.


**Subject-independent models evaluated on a single**
**dataset** should use LOO or K-fold cross-validation

as long as subject-independence is guaranteed.
Sample-based metrics aggregate all samples of individual subject. Overall performance is reported as
the average of all subjects. Event-based metrics aggregate all events in the same manner. All four datasets
can be evaluated. However, for the TUH EEG Seizure
Corpus, the fixed split of training, validation and test
data provided by the original dataset is used.


**Subject-independent** **models** **evaluated** **across**
**datasets** are trained on a single dataset and tested
on the other datasets to verify generalization properties. Sample-based metrics aggregate all samples of
individual subject, and then calculate mean performance over all subjects. Event-based metrics aggregate all events in the same manner.


**3.3 Reporting**


The algorithm should report performance for samplebased and event-based scoring including sensitivity,
precision, F1-score and false-alarms per day for each
individual subject (if possible) and overall average of
all subjects. In addition, algorithms should provide
enough details to allow result reproducibility, e.g. in
a model card including model description, software
and environment documentation, data used, evaluation metrics, and results [38]. An example of such
a model card is provided in Appendix C. To help
authors document and report results we provide a
checklist for reproducible SzCORE algorithms which
can be found in Appendix C.


To test the validity of the framework and as an initial contribution to the benchmark, we ran SzCORE
with three algorithms. The performance results of
these algorithms are presented in appendix B.


**8**


#### **4 Open source library &** **benchmark platform**

Along with a description of the framework and
benchmark, we provide an open-source code library available on GitHub: `[https://github.com/](https://github.com/esl-epfl/sz-validation-framework)`
`[esl-epfl/sz-validation-framework](https://github.com/esl-epfl/sz-validation-framework)` . In its present
form, the library provides functionality to perform
the following actions.


 - Convert EEG data from the main public datasets
to standardized BIDS-EEG compliant format.

 - Convert seizure annotations from the main public datasets to standardized HED-SCORE com
pliant format.

 - Computing the performance of algorithms using
event- or sample-based metrics.


The framework, benchmark and supporting code library are described on an online platform: `[https://](https://eslweb.epfl.ch/epilepsybenchmarks)`
`[eslweb.epfl.ch/epilepsybenchmarks](https://eslweb.epfl.ch/epilepsybenchmarks)`, which also
serves as the central hub for a community-built
benchmark of seizure detection algorithms. The platform allows researchers to upload results of a seizure
detection algorithm following the framework and
benchmark described here. All results are presented
in comparative tables and charts. The platform is
designed to allow continuous improvement by the
community.

#### **5 Discussion**


In this paper, we present SzCORE, a framework for
the validation of EEG-based seizure detection algorithms, and suggest common future research practices, with the aim of allowing fair comparison of
performance results and increasing reproducibility
of studies. This framework is the result of in-depth
discussions with stakeholders from both the medical

and computer science communities.
The present framework defines standards for EEG
datasets based on existing guidelines and recommendations. It also defines data formats for EEG and
seizure annotations that comply with the BIDS-EEG
data organization and HED-SCORE nomenclature. It


provides recommendations and checklist for sound
cross-validation of algorithms and defines performance metrics for their evaluation.


Based on this framework, we propose the _10-20_
_seizure detection benchmark_ . The benchmark defines
the datasets, task and performance metrics to evaluate seizure detection algorithms. Additionally, we
provide an open-source library to convert data from
the public datasets to a standardized data format
along with code that implement the performance
metrics.


Previous initiatives compared algorithms in the
context of contests associated with signal processing
congresses (e.g. Neureka IEEE SPMB 2020 [39, 40],
ICASSP 2023 seizure detection challenge [41, 42]).
However, evaluation data were not always available
after the event, precluding further elaboration or comparison with subsequent algorithms. In contrast, the
present benchmark relies on public datasets and it
provides a fully transparent evaluation framework,
which will hopefully enable continuing progress in
the field.


The proposed benchmark could also be compared
to existing commercial algorithms, which are still less
performant than human experts but have nonetheless
already found some use in the clinic [10, 43].


The choice of 10-20 scalp-EEG recording content
that lies at the core of the present framework is restricted to the minimum recording standards that
are recommended for EMU settings [31]. These are,
however, not met by some highly promising developments in long-term EEG, particularly ambulatory
wearable EEG and subcutaneous EEG, which tend
to use a low number of electrodes positioned in nonstandard locations [6, 5]. Whereas our choice appears to exclude such recordings, it can be argued
that, whenever possible, recording data with the recommended EMU standards in addition to a novel

EEG recording setup guarantees high quality datasets
while allowing for the development of specific benchmarks, for example targeting wearable EEG. This
was the case for the SeizeIT dataset and ICASSP

2023 seizure detection challenge, which included
electrodes positioned behind the ear in addition to
standard 10-20 EEG electrodes [41]. In the future,
we can expect new guidelines for recording EEG in
non-standard locations or different applications that
guarantee high-quality datasets. These new recording standards can use the EEG data format defined
in this framework such that they integrate seamlessly
with the proposed SzCORE evaluation methodology
and performance metrics. They will then be used to
extend the online platform by setting up new datasets
and benchmarks that specifically target those applications.



The presented framework extends previous work
that defined seizure scoring [30] by complementing
sample-based with event-based scoring. The current
choice of parameters for these scoring methods is
somewhat arbitrary if pragmatic. Ideally, the choice
of these parameters should either correspond to a
specific use of seizure detection algorithms or be
based on known uncertainty. Specific use may require high accuracy, e.g. prompt intervention triggered by seizure alarms. Other uses benefit from
high tolerance, e.g. offline review of recordings. In
addition, human expert labeling (with is the current gold-standard) shows variation [44], resulting in
some uncertainty in labeling the start and end time
of seizures [34, 35]. Our choice in this respect was
dictated by the framework, which aims to be generic
and fit a wide range of algorithms and application.
Some users of the framework might want to adapt
some of the parameters to their own use case.
This work effectively addresses some current key
issues relating to the validation of seizure detection
algorithms [28, 29], including the difficulty in comparing results from different datasets and risks associated with a lack of data independence in crossvalidation. The best level of evidence for validation is

reached when based on an independent multi-centric
dataset with strong generalizability potential. Such a
dataset would contain many recordings from different centers from many subjects, including a variety
of seizure types, recording equipment, recording protocol, etc. As this may be difficult to obtain, we give
recommendation for cross-validation strategies that
ensure independence within a single dataset. Future
work from the community should aim at collecting
a large multi-centric dataset that can be used for the
validation of seizure detection algorithms.

#### **6 Conclusion**


This SzCORE framework and benchmark should fos
ter reproducible, transparent, and efficient research.
Crucially, they allow the standardization of the validation of seizure detection algorithms. This will
enable direct comparison of reported results that
use this benchmark. We also provide well-described
performance metrics that are tailored to both the
machine-learning and medical communities. The
framework, benchmark and accompanying opensource software libraries lower the technical and

domain-specific knowledge required for algorithm
developers to work on seizure detection algorithms,
and test them on multiple datasets. The benchmark
will also allow to measure the state of the art of

seizure detection algorithms, and guide new research

venues.


**9**


Moreover, resulting algorithms can serve educational purposes in epilepsy teaching by providing
computer-assistant supervision of epileptologists in
training worldwide. This is in line with recent recommendations of the Intersectoral Global Action Plan

approved by the World Health Organization in 2022,
which promotes prioritization of education, training,
and improving access to care, including in low- and
middle-income countries [45].
The benchmark has the potential for further expansion. As more high-quality and ambulatory datasets
become available, they can better reflect the range of
applications of algorithms. Beyond the detection of
epileptic seizures on scalp-EEG, the development of
the benchmark can address other EEG features and

other physiological signals.
In order to encourage the adoption of the
framework, we have set up a community online platform to describe it and collect results of
algorithms that use it `[https://eslweb.epfl.ch/](https://eslweb.epfl.ch/epilepsybenchmarks)`
`[epilepsybenchmarks](https://eslweb.epfl.ch/epilepsybenchmarks)` . We welcome any suggestions
for new datasets, new tasks, or improvements to the
methodology or content.

#### **Acknowledgements**


The Pedesite consortium participated in this study
through critical feedback on the proposed methodology. In particular the following individuals
(some in the author list) were involved : Alireza
Amirashi [1], David Atienza [1], Jonathan Dan [1], Jose
Miranda [1], Una Pale [1], Amirhossein Shahbaziniae [1],
William Cappelletti [2], Abdellah Rahmani [2], Adriano
Bernini [3], Alexandre Pfister [3], Philippe Ryvlin [3], Antoine Spahr [3], Simone Benatti [4, 5], Luca Benini [4, 5], Andrea Cossettini [4], Thorir Mar Ingolfsson [4], Xiaying
Wang [4] .


1. Embedded Systems Laboratory, EPFL, Switzerland

2. LTS4, EPFL, Switzerland
3. Service of neurology, Centre Hospitalier Universitaire Vaudois, Switzerland
4. Integrated Systems Laboratory, ETH Zürich,
Switzerland

5. Department of Electrical, Electronic and Information Engineering (DEI), University of Bologna,
Italy


In addition we would like to thank the many international collaborators who participated in discussions that helped build this work. In particular the
participants of the Fourth International Congress on
Mobile Health and Digital Technology in Epilepsy
(2023); Christos Chatzichristos, Lauren Swinnen,
Jaiver Macea and Nick Seeuws from KU Leuven


**10**



(Belgium); Bernard Dan, Karine Pelc from ULB (Belgium).

#### **Author contributions**


 - Jonathan Dan: Conceptualization, Methodology,
Software, Validation, Data Curation, Writing, Visualization, Project administration

 - Una Pale: Conceptualization, Methodology, Software, Investigation, Writing, Visualization

 - Alireza Amirshahi: Methodology, Investigation,
Writing – Original Draft

 - William Cappelletti: Methodology

 - Thorir Mar Ingolfsson: Methodology, Investigation, Writing – Original Draft

 - Xiaying Wang: Writing – Review & Editing

 - Andrea Cossettini: Writing – Review & Editing,
Supervision

 - Adriano Bernini: Methodology

 - Luca Benini: Writing – Review & Editing, Supervision, Funding acquisition

 - Sándor Beniczky: Writing – Review & Editing,
Supervision

 - David Atienza: Writing – Review & Editing, Supervision, Funding acquisition

 - Philippe Ryvlin: Methodology, Writing – Review
& Editing, Supervision, Funding acquisition

#### **References**


[1] Christoph Baumgartner and Johannes P. Koren.
“Seizure detection using scalp-EEG”. In: _Epilep-_
_sia_ 59 (June 2018), pp. 14–22. doi: `[10.1111/EPI.](https://doi.org/10.1111/EPI.14052)`

`[14052](https://doi.org/10.1111/EPI.14052)` .


[2] Brad K. Kamitaki et al. “Yield of conventional
and automated seizure detection methods in

the epilepsy monitoring unit”. In: _Seizure_ 69
(July 2019), pp. 290–295. doi: `[10 . 1016 / j .](https://doi.org/10.1016/j.seizure.2019.05.019)`

`[seizure.2019.05.019](https://doi.org/10.1016/j.seizure.2019.05.019)` .


[3] Tasneem F. Hasan and William O. Tatum. “Ambulatory EEG Usefulness in Epilepsy Management”. In: _Journal of Clinical Neurophysiology_ 38
(2 Mar. 2021), pp. 101–111. doi: `[10.1097/WNP.](https://doi.org/10.1097/WNP.0000000000000601)`

`[0000000000000601](https://doi.org/10.1097/WNP.0000000000000601)` .


[4] William O. Tatum, Nimit Desai, and Anteneh
Feyissa. “Ambulatory EEG: Crossing the divide
during a pandemic”. In: _Epilepsy & Behavior_
_Reports_ 16 (Jan. 2021), p. 100500. doi: `[10.1016/](https://doi.org/10.1016/J.EBR.2021.100500)`

`[J.EBR.2021.100500](https://doi.org/10.1016/J.EBR.2021.100500)` .


[5] Sigge Weisdorf et al. “Ultra-long-term subcutaneous home monitoring of epilepsy—490 days
of EEG from nine patients”. In: _Epilepsia_ 60
(Nov. 2019), pp. 2204–2214. doi: `[10.1111/EPI.](https://doi.org/10.1111/EPI.16360)`

`[16360](https://doi.org/10.1111/EPI.16360)` .


[6] Jaiver Macea et al. “In-hospital and homebased long-term monitoring of focal epilepsy
with a wearable electroencephalographic device: Diagnostic yield and user experience”.
In: _Epilepsia_ 64 (4 Apr. 2023), pp. 937–950. doi:
`[10.1111/EPI.17517](https://doi.org/10.1111/EPI.17517)` .


[7] Giorgi Japaridze et al. “Automated detection
of absence seizures using a wearable electroencephalographic device: a phase 3 validation
study and feasibility of automated behavioral
testing”. In: _Epilepsia_ 64 (Dec. 2022), S40–S46.
doi: `[10.1111/EPI.17200](https://doi.org/10.1111/EPI.17200)` .


[8] Ralph G. Andrzejak et al. “Seizure forecasting:
Where do we stand?” In: _Epilepsia_ (2023). doi:
`[10.1111/EPI.17546](https://doi.org/10.1111/EPI.17546)` .


[9] Palak Handa, Monika Mathur, and Nidhi Goel.
“EEG Datasets in Machine Learning Applications of Epilepsy Diagnosis and Seizure Detection”. In: _SN Computer Science_ 4 (5 Sept. 2023),
pp. 1–11. doi: `[10.1007/S42979-023-01958-Z](https://doi.org/10.1007/S42979-023-01958-Z)` .


[10] Elisabeth E.M. Reus et al. “Automated seizure
detection in an EMU setting: Are software packages ready for implementation?” In: _Seizure_
96 (Mar. 2022), pp. 13–17. doi: `[10 . 1016 / J .](https://doi.org/10.1016/J.SEIZURE.2022.01.009)`

`[SEIZURE.2022.01.009](https://doi.org/10.1016/J.SEIZURE.2022.01.009)` .


[11] Jia Deng et al. “ImageNet: A large-scale hierarchical image database”. In: (Mar. 2010), pp. 248–
255. doi: `[10.1109/CVPR.2009.5206848](https://doi.org/10.1109/CVPR.2009.5206848)` .


[12] Pranav Rajpurkar et al. “SQuAD: 100,000+
Questions for Machine Comprehension of
Text”. In: _Proceedings of the 2016 Conference on_
_Empirical Methods in Natural Language Process-_
_ing_ . Ed. by Jian Su, Kevin Duh, and Xavier Carreras. Austin, Texas: Association for Computational Linguistics, Nov. 2016, pp. 2383–2392.
doi: `[10.18653/v1/D16-1264](https://doi.org/10.18653/v1/D16-1264)` .


[13] Martin Schrimpf et al. “Integrative Benchmarking to Advance Neurally Mechanistic Models
of Human Intelligence”. In: _Neuron_ 108 (3 Nov.
2020), pp. 413–423. doi: `[10.1016/j.neuron.](https://doi.org/10.1016/j.neuron.2020.07.040)`

`[2020.07.040](https://doi.org/10.1016/j.neuron.2020.07.040)` .


[14] Jonathan Dan et al. “Computationally-efficient
algorithm for real-time absence seizure detection in wearable electroencephalography”. In:
_Int. J. Neural Syst._ 30 (11 Nov. 2020), p. 2050035.
doi: `[10.1142/s0129065720500355](https://doi.org/10.1142/s0129065720500355)` .




[15] Christos Chatzichristos et al. “Multimodal detection of typical absence seizures in home
environment with wearable electrodes”. In:

_Frontiers in Signal Processing_ 2 (Oct. 2022),
p. 1014700. doi: `[10 . 3389 / FRSIP . 2022 .](https://doi.org/10.3389/FRSIP.2022.1014700)`

`[1014700](https://doi.org/10.3389/FRSIP.2022.1014700)` .


[16] Punnawish Thuwajit et al. “EEGWaveNet: Multiscale CNN-Based Spatiotemporal Feature Extraction for EEG Seizure Detection”. In: _IEEE_
_Transactions on Industrial Informatics_ 18 (8 Aug.
2022), pp. 5547–5557. doi: `[10.1109/TII.2021.](https://doi.org/10.1109/TII.2021.3133307)`

`[3133307](https://doi.org/10.1109/TII.2021.3133307)` .


[17] Ali Hossam Shoeb. “Application of machine
learning to epileptic seizure onset detection
and treatment”. Massachusetts Institute of

Technology, Sept. 2009.


[18] Ary L. Goldberger et al. “PhysioBank, PhysioToolkit, and PhysioNet: components of a new
research resource for complex physiologic signals”. In: _Circulation_ 101 (23 2000). doi: `[10 .](https://doi.org/10.1161/01.CIR.101.23.E215)`
`[1161/01.CIR.101.23.E215](https://doi.org/10.1161/01.CIR.101.23.E215)` .


[19] Vinit Shah et al. “The temple university hospital seizure detection corpus”. In: _Frontiers in_
_Neuroinformatics_ 12 (Nov. 2018), p. 357250. doi:
`[10.3389/FNINF.2018.00083](https://doi.org/10.3389/FNINF.2018.00083)` .


[20] Paolo Detti. _Siena Scalp EEG Database v1.0.0_ .
Physionet. 2020. doi: `[https://doi.org/10.](https://doi.org/https://doi.org/10.13026/5d4a-j060)`
`[13026/5d4a-j060](https://doi.org/https://doi.org/10.13026/5d4a-j060)` .


[21] Paolo Detti, Giampaolo Vatti, and Garazi Zabalo Manrique de Lara. “EEG Synchronization Analysis for Seizure Prediction: A Study
on Data of Noninvasive Recordings”. In: _Pro-_
_cesses_ 8 (7 July 2020), p. 846. doi: `[10.3390/](https://doi.org/10.3390/PR8070846)`

`[PR8070846](https://doi.org/10.3390/PR8070846)` .


[22] Christos Chatzichristos and Miguel Claro
Bhagubai. _SeizeIT1_ . KU Leuven RDR. Version v1.0.0. 2023. doi: `[10.48804/P5Q0OJ](https://doi.org/10.48804/P5Q0OJ)` .


[23] Sándor Beniczky et al. “Standardized
computer-based organized reporting of EEG:
SCORE - Second version”. In: _Clinical Neuro-_

_physiology_ 128 (11 Nov. 2017), pp. 2334–2346.
doi: `[10.1016/J.CLINPH.2017.07.418](https://doi.org/10.1016/J.CLINPH.2017.07.418)` .


[24] Krzysztof J. Gorgolewski et al. “The brain imaging data structure, a format for organizing
and describing outputs of neuroimaging experiments”. In: _Scientific Data_ 3 (1 June 2016),
pp. 1–9. doi: `[10.1038/sdata.2016.44](https://doi.org/10.1038/sdata.2016.44)` .


[25] Cyril R. Pernet et al. “EEG-BIDS, an extension
to the brain imaging data structure for electroencephalography”. In: _Scientific Data_ 6 (1
June 2019), pp. 1–5. doi: `[10.1038/s41597-019-](https://doi.org/10.1038/s41597-019-0104-8)`

`[0104-8](https://doi.org/10.1038/s41597-019-0104-8)` .


**11**


[26] Tal Pal Attia et al. _Hierarchical Event Descriptor_
_library schema for EEG data annotation_ . Oct. 2023.
doi: `[10.48550/arXiv.2310.15173](https://doi.org/10.48550/arXiv.2310.15173)` .


[27] Payam Refaeilzadeh, Lei Tang, and Huan Liu.
“Cross-Validation”. In: _Encyclopedia of Database_
_Systems_ . Ed. by Ling Liu and M. Tamer Özsu.
Boston, MA: Springer US, 2009, pp. 532–538.
doi: `[10.1007/978-0-387-39940-9_565](https://doi.org/10.1007/978-0-387-39940-9_565)` .


[28] Sina Shafiezadeh et al. “Methodological Issues
in Evaluating Machine Learning Models for
EEG Seizure Prediction: Good Cross-Validation

Accuracy Does Not Guarantee Generalization
to New Patients”. In: _Applied Sciences 2023, Vol._
_13, Page 4262_ 13 (7 Mar. 2023), p. 4262. doi:
`[10.3390/APP13074262](https://doi.org/10.3390/APP13074262)` .


[29] Una Pale, Tomas Teijeiro, and David Atienza.
“Importance of methodological choices in data
manipulation for validating epileptic seizure
detection models”. In: _Proceedings of the 2023_
_45th Annual International Conference of the IEEE_
_Engineering in Medecine and Biology Society_
_(EMBC)_ . Sidney, Australia: IEEE, 2023. doi: `[10.](https://doi.org/10.13039/501100011033)`
`[13039/501100011033](https://doi.org/10.13039/501100011033)` .


[30] Vinit Shah et al. “Objective Evaluation Metrics
for Automatic Classification of EEG Events”. In:
_Biomedical Signal Processing_ (2021), pp. 223–255.
doi: `[10.1007/978-3-030-67494-6_8](https://doi.org/10.1007/978-3-030-67494-6_8)` .


[31] Maria E. Peltola et al. “Routine and sleep EEG:
Minimum recording standards of the International Federation of Clinical Neurophysiology and the International League Against
Epilepsy”. In: _Epilepsia_ 64 (3 Mar. 2023),
pp. 602–618. doi: `[10.1111/EPI.17448](https://doi.org/10.1111/EPI.17448)` .


[32] Ingrid E. Scheffer et al. “ILAE classification of
the epilepsies: Position paper of the ILAE Commission for Classification and Terminology”.
In: _Epilepsia_ 58 (4 Apr. 2017), pp. 512–521. doi:
`[10.1111/EPI.13709](https://doi.org/10.1111/EPI.13709)` .


[33] Trevor Hastie, Robert Tibshirani, and Jerome
Friedman. “Model Assessment and Selection”.

In: _The Elements of Statistical Learning: Data Min-_
_ing, Inference, and Prediction_ . New York, NY:
Springer New York, 2009, pp. 219–259. doi:
`[10.1007/978-0-387-84858-7_7](https://doi.org/10.1007/978-0-387-84858-7_7)` .


[34] Buajieerguli Maimaiti et al. “An Overview
of EEG-based Machine Learning Methods
in Seizure Prediction and Opportunities for
Neurologists in this Field”. In: _Neuroscience_
481 (2022), pp. 197–218. doi: `[10 . 1016 / j .](https://doi.org/10.1016/j.neuroscience.2021.11.017)`

`[neuroscience.2021.11.017](https://doi.org/10.1016/j.neuroscience.2021.11.017)` .


**12**




[35] Ali Shoeb et al. “A machine-learning algorithm
for detecting seizure termination in scalp EEG”.
In: _Epilepsy & Behavior_ 22 (2011), S36–S43. doi:
`[10.1016/j.yebeh.2011.08.040](https://doi.org/10.1016/j.yebeh.2011.08.040)` .


[36] Eugen Trinka et al. “A definition and classification of status epilepticus – Report of the ILAE
Task Force on Classification of Status Epilepticus”. In: _Epilepsia_ 56 (10 Oct. 2015), pp. 1515–
1523. doi: `[10.1111/EPI.13121](https://doi.org/10.1111/EPI.13121)` .


[37] Sheng Wong et al. “EEG datasets for seizure detection and prediction— A review”. In: _Epilep-_
_sia Open_ 8 (2 June 2023), pp. 252–267. doi: `[10.](https://doi.org/10.1002/EPI4.12704)`
`[1002/EPI4.12704](https://doi.org/10.1002/EPI4.12704)` .


[38] Margaret Mitchell et al. “Model Cards for
Model Reporting”. In: _Proceedings of the Confer-_
_ence on Fairness, Accountability, and Transparency_ .
FAT* ’19. Atlanta, GA, USA: Association for
Computing Machinery, 2019, pp. 220–229. doi:
`[10.1145/3287560.3287596](https://doi.org/10.1145/3287560.3287596)` .


[39] _Neureka IEEE SPMB 2020_ . `[https://neureka-](https://neureka-challenge.com)`
`[challenge.com](https://neureka-challenge.com)` . Accessed: 12-12-2023.


[40] Christos Chatzichristos et al. “Epileptic Seizure
Detection in EEG via Fusion of Multi-View

Attention-Gated U-Net Deep Neural Networks”. In: _2020 IEEE Signal Processing in_
_Medicine and Biology Symposium_ (Dec. 2020).
doi: `[10.1109/SPMB50085.2020.9353630](https://doi.org/10.1109/SPMB50085.2020.9353630)` .


[41] _Seizure detection challenge – IEEE ICASSP 2023_ .
```
   https : / / signalprocessingsociety . org /
   publications-resources/data-challenges/
   seizure - detection - challenge - icassp ```

`[2023](https://signalprocessingsociety.org/publications-resources/data-challenges/seizure-detection-challenge-icassp-2023)` . Accessed: 12-12-2023.


[42] Irfan Al-Hussaini and Cassie S. Mitchell.
“SeizFt: Interpretable Machine Learning for
Seizure Detection Using Wearables”. In: _Bio-_
_engineering_ 10.8 (2023). doi: `[10 . 3390 /](https://doi.org/10.3390/bioengineering10080918)`
`[bioengineering10080918](https://doi.org/10.3390/bioengineering10080918)` .


[43] Johannes Koren et al. “Systematic analysis and
comparison of commercial seizure-detection
software”. In: _Epilepsia_ 62.2 (2021), pp. 426–438.
doi: `[10.1111/epi.16812](https://doi.org/10.1111/epi.16812)` .


[44] Jonathan J. Halford et al. “Inter-rater Agreement on Identification of Electrographic
Seizures and Periodic Discharges in ICU EEG
Recordings”. In: _Clinical neurophysiology_ 126 (9
Sept. 2015), p. 1661. doi: `[10.1016/J.CLINPH.](https://doi.org/10.1016/J.CLINPH.2014.11.008)`

`[2014.11.008](https://doi.org/10.1016/J.CLINPH.2014.11.008)` .


[45] Alla Guekht et al. “The road to a World Health
Organization global action plan on epilepsy
and other neurological disorders”. In: _Epilepsia_
62.5 (2021), pp. 1057–1063. doi: `[10.1111/epi.](https://doi.org/10.1111/epi.16856)`

`[16856](https://doi.org/10.1111/epi.16856)` .


[46] Steven N. Baldassano et al. “Crowdsourcing
seizure detection: algorithm development and
validation on human implanted device recordings”. In: _Brain_ 140 (6 June 2017), pp. 1680–1691.
doi: `[10.1093/BRAIN/AWX098](https://doi.org/10.1093/BRAIN/AWX098)` .


[47] Dionisije Sopic, Amir Aminifar, and David
Atienza. “e-Glass: A Wearable System for RealTime Detection of Epileptic Seizures”. In: _2018_
_IEEE International Symposium on Circuits and_
_Systems (ISCAS)_ . 2018, pp. 1–5. doi: `[10.1109/](https://doi.org/10.1109/ISCAS.2018.8351728)`

`[ISCAS.2018.8351728](https://doi.org/10.1109/ISCAS.2018.8351728)` .


[48] Mohammad Khubeb Siddiqui et al. “A review
of epileptic seizure detection using machine
learning classifiers”. In: _Brain Informatics_ 7 (1
Dec. 2020), pp. 1–18. doi: `[10.1186/S40708-](https://doi.org/10.1186/S40708-020-00105-1/TABLES/3)`
`[020-00105-1/TABLES/3](https://doi.org/10.1186/S40708-020-00105-1/TABLES/3)` .


[49] Renato Zanetti et al. “Approximate zerocrossing: a new interpretable, highly discriminative and low-complexity feature for EEG and
iEEG seizure detection”. In: _Journal of Neural_
_Engineering_ 19.6 (Nov. 25, 2022). doi: `[10.1088/](https://doi.org/10.1088/1741-2552/aca1e4)`
`[1741-2552/aca1e4](https://doi.org/10.1088/1741-2552/aca1e4)` .


[50] Alessio Burrello et al. “Laelaps: An EnergyEfficient Seizure Detection Algorithm from
Long-term Human iEEG Recordings without
False Alarms”. In: _Proceedings of the 2019 De-_
_sign, Automation & Test in Europe Conference &_
_Exhibition (DATE)_ . Florence, Italy: IEEE, 2019.
doi: `[10.23919/DATE.2019.8715186](https://doi.org/10.23919/DATE.2019.8715186)` .


[51] Yongpei Ma et al. “TSD: Transformers for
Seizure Detection”. In: _bioRxiv_ (2023), pp. 2023–
01. doi: `[10.1101/2023.01.24.525308](https://doi.org/10.1101/2023.01.24.525308)` .


[52] Alexey Dosovitskiy et al. “An Image is Worth
16x16 Words: Transformers for Image Recognition at Scale”. In: _International Conference on_
_Learning Representations_ . 2021.


[53] Thorir Mar Ingolfsson et al. “Towards longterm non-invasive monitoring for epilepsy via
wearable eeg devices”. In: _2021 IEEE Biomedical_
_Circuits and Systems Conference (BioCAS)_ . IEEE.
2021, pp. 01–04.


[54] Joelle Pineau et al. “Improving Reproducibility in Machine Learning Research (A Report
from the NeurIPS 2019 Reproducibility Program)”. In: _Journal of Machine Learning Research_
22 (2021), pp. 1–20.



**13**


#### **A Data format**

**A.1 BIDS-EEG compliant dataset**


Here we present the file structure organization of the Physionet CHB-MIT Scalp EEG Database converted to
BIDS-EEG [24, 25]. Annotations from seizure detection algorithms are placed in the `szDetection` derivatives
folder that can be distributed with or without the original dataset. The CHB-MIT dataset converted to
BIDS-EEG is made available on zenodo: `[https://zenodo.org/records/10259996](https://zenodo.org/records/10259996)` .

```
BIDS_CHB-MIT/

  README

  dataset_description.json

  events.json

  participants.json

  participants.tsv
  sub-01/

    ses-01/

      eeg/
        sub-01_ses-01_task-szMonitoring_run-00_eeg.edf
        sub-01_ses-01_task-szMonitoring_run-00_eeg.json
        sub-01_ses-01_task-szMonitoring_run-00_events.tsv

        ...

    ...

  ...

  szDetection/

    sub-01/

      ses-01/

        sub-01_ses-01_task-szMonitoring_run-00_events.tsv

```

**A.2 Annotation format**


The annotation format is a tab-separated values ( `tsv` ) file. It is HED-SCORE compliant. It contains the
following information:


**onset** represents the start time of the event from the beginning of the recording, in seconds.
**duration** represents the duration of the event, in seconds.
**event** indicates the type of the event. The event field is primarily used to describe the seizure type. Seizure
events begin with the value `sz` . They can optionally contain more detailed seizure types, as shown in
Figure 4. Recordings with no seizures use the string `bckg` with the event duration equal to the recording
duration.

**confidence** represents confidence in the event label. Values are in the range [0–1] [no confidence – fully
confident]. This field is intended for the confidence of the output prediction of machine learning
algorithms. It is optional, if it is not provided value should be `n/a` .
**channels** represents channels to which the event label applies. If the event applies to all channels, it is marked
with the value `all` . Channels are listed with coma-separated values. It is optional, if it is not provided
value should be `n/a` .
**dateTime** start date time of the recording file. The date time is specified in the `POSIX` format `%Y-%m-%d`
`%H:%M:%S` (e.g., 2023-07-24 13:58:32). The start time of a recording file is often specified in the metadata of
the `edf` .

**recordingDuration** refers to the total duration of the recording file in seconds.

```
 onset duration eventType confidence channels dateTime recordingDuration
 296.0 40.0 sz n/a n/a 2016 -11 -06 13:43:04 3600.00

 453.0 12.0 sz n/a n/a 2016 -11 -06 13:43:04 3600.00

 895.0 21.0 sz n/a n/a 2016 -11 -06 13:43:04 3600.00

```

_An annotation file that contains three seizures._


**14**


![](/mnt/c/Users/JJ/Desktop/Clarity-Digital-Twin/SeizureTransformer/literature/markdown/SzCORE/SzCORE.pdf-14-4.png)

![](/mnt/c/Users/JJ/Desktop/Clarity-Digital-Twin/SeizureTransformer/literature/markdown/SzCORE/SzCORE.pdf-14-5.png)

![](/mnt/c/Users/JJ/Desktop/Clarity-Digital-Twin/SeizureTransformer/literature/markdown/SzCORE/SzCORE.pdf-14-6.png)

![](/mnt/c/Users/JJ/Desktop/Clarity-Digital-Twin/SeizureTransformer/literature/markdown/SzCORE/SzCORE.pdf-14-7.png)

**Figure 4:** _ILAE 2017 Classification of seizure types (expanded version) [32] Items in purple are used as short codes to describe an_
_event. As an example a generalized tonic-clonic seizure would be given the code:_ _`sz-gen-m-tonic_clonic`_ _._


We propose to adopt the ILAE classification of seizure types to describe seizure types [32] stored in the event
field. The classification is hierarchical, depending on available clinical information. At the top level, the seizure
type is unspecified ( `sz` ). The second level describes the seizure onset zone (focal: `sz-foc`, generalized `sz-gen`
or unknown `sz-uon` ). Further levels describe the awareness, motor components and seizure symptomology.
The full list of standardized seizure types is presented in Figure 4. They are linked to the hierarchy defined by
HED-SCORE. The mapping to HED tags is provided in the BIDS-EEG converter library.

#### **B Benchmark**


Here we describe three algorithms that implement the 10-20 seizure detection benchmark.


**B.1 Algorithms**


**Random forest with Approximate zero-cross features** This random forest is lightweight model that performs
relatively well for epileptic seizure detection. It has been extensively used for EEG-based seizure classification [46, 47, 48]. A recent paper by Zanetti et al. [49] demonstrated that six approximate zero-crossing (AZC)
features can outperform a set of classical literature features (CLF) on two publicly available datasets: CHB-MIT


**15**


**Table 2:** _Performance metrics of subject-independent seizure detection algorithms trained on a single dataset and evaluated on the_
_same dataset using cross-validation._


Model Metrics Event-based Sample-based
CHB-MIT TUH Siena SeizeIT CHB-MIT TUH Siena SeizeIT


RF F1-score 53.9 59.3 21.7 19.8

Sensitivity 37.0 32.9 10.8 6.8
Precision 64.5 62.5 71.9 69.8

FP/day 1.66 1.7         -         

Transformer F1-score 63.2 22.8 61.6 17.3

Sensitivity 76.5 56.9 60.7 23.3
Precision 53.9 18.7 62.4 69.9

FP/day 40.6 34.4         - 21.1


XGBoost F1-score 66.0 52.0

Sensitivity 67.1 48.14
Precision 75.3 52.19

FP/day 2.09         

(scalp EEG) and SWEC-ETHZ (intracranial EEG) [50]. The hyperparameters are an ensemble of 100 decision
trees built with the Gini split criterion.


**Transformer** In this model, a short-time Fourier transform (STFT) is applied to 12-second windows of EEG.
The STFT is computed on one-second segments, 50 samples of overlap, and a frequency resolution of 2 Hz.
These parameter choices are extracted from the recommendations in [51]. The model used for this task is a
4-layer VisionTransformer-based model [52], which is modified for epileptic seizure detection by [51]. The
STFT extracted from the EEG input signal is considered as an input image to this 4-layer transformer encoder.
The decoder is implemented as a fully connected layer, reducing the dimensions to match the number of
classes.


**XGBoost** In their seminal work, Ingolfsson et al. [53] demonstrated the efficacy of Discrete Wavelet Transform
(DWT) attributes as robust discriminators for seizure events when integrated into classical machine learning
architectures such as Random Forests and Decision Trees. Building upon this foundation, the algorithms
enriches this paradigm by incorporating Gradient Boosted Trees — specifically, the advanced eXtreme Gradient
Boosting (XGBoost) framework. The approach exploits the discriminative power of DWT features in synergy
with XGBoost. In addition, Approximate zero-cross features explained in the section above are provided to the
algorithm. The window size is set to 1 second.


**B.2 Results**


**16**


**Table 3:** _Performance metrics of subject-independent seizure detection algorithms trained on a dataset and evaluated on independent_
_datasets._


Model Metrics Training Event-based Sample-based
data CHB-MIT TUH Siena SeizeIT CHB-MIT TUH Siena SeizeIT


RF F1-score Siena 21.2 _|_ 11.1
Sensitivity Siena 22.2 _|_ 7.1
Precision Siena 20.4 _|_ 20.9
FP/day Siena 2.23 _|_        

RF F1-score CHB-MIT _|_ 41.8 _|_ 13.9
Sensitivity CHB-MIT _|_ 48.9 _|_ 8.5
Precision CHB-MIT _|_ 52.5 _|_ 64.9
FP/day CHB-MIT _|_ 9.4 _|_        

Transformer F1-score TUH _|_ 32.2 _|_ 26.8
Sensitivity TUH _|_ 54.4 _|_ 28.9
Precision TUH _|_ 31.3 _|_ 35.9
FP/day TUH _|_ 21.9 _|_        

XGBoost F1-score

Sensitivity

Precision


FP/day


**Table 4:** _Performance metrics of subject-specific models_


Model Metrics Event-based Sample-based
CHB-MIT TUH* Siena SeizeIT CHB-MIT TUH* Siena SeizeIT


RF F1-score 72.7  - 58.8 51.7  - 36.0

Sensitivity 74.0          - 62.8 40.0          - 26.8
Precision 77.5          - 55.6 82.7          - 65.2

FP/day 1.58        - 4.64        -        -        

Transformer F1-score  -  
                               -                               Sensitivity
Precision          -          
                               -                               FP/day


XGBoost F1-score 79.8  - 60.5  
Sensitivity 87.36          - 54.63          Precision 80.14          - 77.75          
FP/day 0.99        -        -        
*TUH is not considered due to insufficient data per subject


**17**


#### **C Model Card & SzCORE Reproducibility Checklist**

In table 5, we provide a template model card for reporting results of seizure detection algorithms. The model
card contains contact details, model details and a standardized presentation of performance results. It is
provided as an editable PDF, a L [A] T E X template and a Microsoft Word template. All of which can be downloaded
here : `[https://eslweb.epfl.ch/epilepsybenchmarks/model-card/](https://eslweb.epfl.ch/epilepsybenchmarks/model-card/)` .
In table 6, we provide a checklist for authors that report results based on the SzCORE framework. The
checklist is based on _The Machine Learning Reproducibility Checklist_ [54].

#### **D Ways to contribute**


This framework and benchmark should foster reproducible, transparent, and efficient research. It will benefit
from contributions from the community. Here, we list several ways to contribute to the framework and
benchmark.


**Feedback**


 - Provide feedback on the proposed framework and benchmark using the following form: `[https://forms.](https://forms.gle/XfbDaJQi2VooWRN2A)`
`[gle/XfbDaJQi2VooWRN2A](https://forms.gle/XfbDaJQi2VooWRN2A)` . We are interested in problems and challenges you might have encountered and
ideas to improve the framework and the platform.

 - Get in touch with us if you need help or are interested in a collaboration. You can contact the corresponding
[author (jonathan.dan@epfl.ch) or any author of the paper.](mailto:jonathan.dan@epfl.ch)


**Contribute to the 10-20 seizure detection benchmark**


 - Report results of your seizure detection and include results of your algorithm on the 10-20 seizure
detection benchmark. The checklist and model card in this paper should help you report results in a
compliant manner.

 - Submit the performance of your algorithm on the online platform: `[https://eslweb.epfl.ch/](https://eslweb.epfl.ch/epilepsybenchmarks)`
`[epilepsybenchmarks](https://eslweb.epfl.ch/epilepsybenchmarks)` . Once validated, your results will be displayed publicly and compared to other
algorithms.

 - Contribute to a new dataset. Our field would benefit from more datasets that can be used for the validation
of seizure detection algorithms. We expect high quality scalp-EEG datasets that adhere to the SzCORE
framework. These could either be made publicly available or could be used as a private test dataset on
the online platform.

 - Contribute to the code libraries that enable the SzCORE framework and benchmark. The different

code libraries are open-source and open to community contributions. You will find them on Github:
`[https://github.com/esl-epfl/sz-validation-framework](https://github.com/esl-epfl/sz-validation-framework)` .


**18**


**Table 5:** _Model Card for reporting results of algorithms validated using SzCORE._



![](/mnt/c/Users/JJ/Desktop/Clarity-Digital-Twin/SeizureTransformer/literature/markdown/SzCORE/SzCORE.pdf-18-0.png)


|Performance of a subject-specific model|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|Col13|Col14|Col15|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Metrics<br>Event-based<br>Sample-based<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|Metrics<br>Event-based<br>Sample-based<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|Metrics<br>Event-based<br>Sample-based<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|Metrics<br>Event-based<br>Sample-based<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|Metrics<br>Event-based<br>Sample-based<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|Metrics<br>Event-based<br>Sample-based<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|Metrics<br>Event-based<br>Sample-based<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|Metrics<br>Event-based<br>Sample-based<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|Metrics<br>Event-based<br>Sample-based<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|Metrics<br>Event-based<br>Sample-based<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|Metrics<br>Event-based<br>Sample-based<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|Metrics<br>Event-based<br>Sample-based<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|Metrics<br>Event-based<br>Sample-based<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|Metrics<br>Event-based<br>Sample-based<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|Metrics<br>Event-based<br>Sample-based<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|
|F1-score<br>Sensitivity<br>Precision<br>FP/day|||-<br>-<br>-<br>-|||||||-<br>-<br>-<br>-|||||
|F1-score<br>Sensitivity<br>Precision<br>FP/day|||||||||||||||
|F1-score<br>Sensitivity<br>Precision<br>FP/day|||||||||||||||
|F1-score<br>Sensitivity<br>Precision<br>FP/day|||||||||||||||


|Performance of a subject-independent model cross-validated on a single dataset|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|Col13|Col14|Col15|Col16|Col17|Col18|Col19|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Metrics<br>Event-based<br>Sample-based<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|Metrics<br>Event-based<br>Sample-based<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|Metrics<br>Event-based<br>Sample-based<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|Metrics<br>Event-based<br>Sample-based<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|Metrics<br>Event-based<br>Sample-based<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|Metrics<br>Event-based<br>Sample-based<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|Metrics<br>Event-based<br>Sample-based<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|Metrics<br>Event-based<br>Sample-based<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|Metrics<br>Event-based<br>Sample-based<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|Metrics<br>Event-based<br>Sample-based<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|Metrics<br>Event-based<br>Sample-based<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|Metrics<br>Event-based<br>Sample-based<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|Metrics<br>Event-based<br>Sample-based<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|Metrics<br>Event-based<br>Sample-based<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|Metrics<br>Event-based<br>Sample-based<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|Metrics<br>Event-based<br>Sample-based<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|Metrics<br>Event-based<br>Sample-based<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|Metrics<br>Event-based<br>Sample-based<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|Metrics<br>Event-based<br>Sample-based<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|
|F1-score<br>Sensitivity<br>Precision<br>FP/day|||||||||||||||||||
|F1-score<br>Sensitivity<br>Precision<br>FP/day|||||||||||||||||||
|F1-score<br>Sensitivity<br>Precision<br>FP/day|||||||||||||||||||
|F1-score<br>Sensitivity<br>Precision<br>FP/day|||||||||||||||||||


|Performance of a subject-independent model trained on a independent dataset|Col2|Col3|Col4|
|---|---|---|---|
|Training<br>Metrics<br>Event-based<br>Sample-based<br>Data<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|Training<br>Metrics<br>Event-based<br>Sample-based<br>Data<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|Training<br>Metrics<br>Event-based<br>Sample-based<br>Data<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|Training<br>Metrics<br>Event-based<br>Sample-based<br>Data<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT<br>CHB-MIT<br>TUH<br>Siena<br>SeizeIT|
||F1-score<br>Sensitivity<br>Precision<br>FP/day|||



**19**


**Table 6:** _SzCORE reproducibility checklist_


**SzCORE Reproducibility Checklist**


For all **models** and **algorithms** presented, check if you include:

 - A clear description of the mathematical setting, algorithm, and/or model including assumptions
and parameters.

 - A description of the input data of the algorithm specifying sampling frequency, and number of
channels.

 - An analysis of the complexity (time, space, sample size) of any algorithm.


For all **datasets** uses, check if you include:

 - A description of the dataset including the number of subjects, number of seizures, seizure type,
and recording duration.

 - The details of the train / validation / test splits that respect subject independence and chronology.

 - An explanation of any data that were excluded, and all pre-processing steps.

 - A link to a downloadable version of the dataset.

 - For new data collected, a complete description of the data collection process, such as instructions
to annotators and methods for quality control along with a BIDS-EEG / HED-SCORE compatible
version of the dataset.


For all share **code** related to this work, check if you include:

 - Specification of dependencies.

 - Training code.

 - Evaluation code.

 - (Pre-)trained model(s).

 - README file includes table of results accompanied by precise command to run to produce results.


For all reported **experimental results**, check if you include:

 - The range of hyper-parameters considered, method to select the best hyper-parameter configuration,
and specification of all hyper-parameters used to generate results.

 - The exact number of training and evaluation runs.

 - A clear definition of the specific measure or statistics used to report results.

 - A description of results with a report of sensitivity, precision, F1-score and false alarm rate per day.

 - A description of results on the publicly available datasets, namely Physionet CHB-MIT Scalp EEG
Database, TUH EEG Seizure Corpus, Physionet Siena Scalp EEG, and SeizIT1.

 - The average runtime for each result, or estimated energy cost.

 - A description of the computing infrastructure used.



**20**


