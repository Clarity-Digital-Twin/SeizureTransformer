# Discussion

## Performance Gap Analysis

Our evaluation reveals a 27-137x gap between SeizureTransformer's reported performance and its clinical reality on TUSZ. The model's ~1 FA/24h achievement on Dianalund becomes 26.89 FA/24h with NEDC OVERLAP and 136.73 FA/24h with NEDC TAES when evaluated on its training dataset. This dramatic variation is not an indictment of SeizureTransformer's architecture, which represents a genuine advance in combining U-Net feature extraction with Transformer sequence modeling. Rather, it exposes fundamental issues in how the field evaluates seizure detection models, where the same predictions can yield vastly different performance metrics depending on evaluation choices.

## Impact of Scoring Methodology

The 3.1x difference in false alarm rates between NEDC OVERLAP (26.89 FA/24h) and SzCORE Event (8.59 FA/24h) on identical predictions demonstrates that scoring methodology alone can determine whether a model appears clinically viable. NEDC TAES, with its strict time-aligned evaluation, shows an even larger 5.1x increase over OVERLAP and a 15.9x increase over SzCORE Event. These differences stem from fundamental philosophical disagreements about what constitutes a correct detection: TAES requires precise temporal alignment and penalizes both over- and under-segmentation through partial credit scoring, OVERLAP accepts any temporal intersection as sufficient, while SzCORE Event adds 30-second pre-ictal and 60-second post-ictal tolerances before applying overlap logic. Each approach serves legitimate clinical purposes—TAES for applications requiring precise seizure boundaries, OVERLAP for standard clinical review, and SzCORE Event for screening where missing events is costlier than false alarms.

Our focus on event-based metrics reflects clinical priorities. While sample-based (epoch) methods (NEDC EPOCH; SzCORE Sample-based) can yield high nominal accuracy by correctly classifying long non-seizure periods, they obscure the core task of detecting seizure events. We therefore restrict comparisons and conclusions to event-based scores.

## Clinical Deployment Constraints

The inability to achieve clinical viability reveals a critical gap between research achievements and deployment readiness. Our best operating point at 10 FA/24h achieved only 33.90% sensitivity with NEDC OVERLAP, falling far short of the 75% sensitivity goal for clinical systems [13]. This constraint is not merely academic—it determines whether AI assistants can be deployed in ICUs, where false alarms cause alarm fatigue and missed seizures delay critical treatment. While human reviewers achieve approximately 1 FA/24h [13], even at a more permissive 10 FA/24h threshold, current models cannot approach the sensitivity levels required for clinical deployment when evaluated with appropriate standards.

## Root Causes of Evaluation Gaps

The performance disparities stem from multiple compounding factors beyond scoring methodology. Dataset characteristics play a crucial role: TUSZ contains 865 evaluation files with diverse seizure types and recording conditions from an urban academic medical center, while Dianalund represents a specialized epilepsy monitoring unit with potentially cleaner recordings and different patient populations. Training choices further compound these differences—SeizureTransformer was trained on TUSZ v2.0.3 combined with the Siena dataset [9], with our evaluation using the same TUSZ v2.0.3 for consistency. The lack of standardized evaluation protocols allows models to be tested on favorable datasets with permissive scoring, creating an illusion of clinical readiness that disappears under rigorous evaluation.

## Systemic Issues in the Field

The 27-137x gap we document is not unique to SeizureTransformer but reflects systemic issues in how seizure detection research approaches evaluation. The field has optimized for benchmark leaderboards rather than clinical deployment, creating incentives to report results on datasets and with scoring methods that maximize apparent performance. EpilepsyBench's use of a train icon to mark TUSZ and withhold TUSZ evaluation metrics, while well-intentioned to ensure held-out testing, can inadvertently discourage evaluating models on TUSZ's held-out split with matched tooling. This creates a situation where models can claim state-of-the-art performance without ever facing the clinical standards they purport to meet.

## Cross-Dataset Validity

Using identical SzCORE Event scoring, SeizureTransformer achieves 1 FA/24h on Dianalund (37% sensitivity) versus 8.59 FA/24h on TUSZ (52.35% sensitivity)—an 8.6× degradation that indicates limited generalization across datasets even under permissive clinical tolerances. This isolates dataset shift from scoring effects. When we further apply TUSZ's standard NEDC OVERLAP scoring, the gap widens to 26.89 FA/24h (27× increase), and with strict NEDC TAES scoring reaches 136.73 FA/24h (137× increase). These cascading gaps—8.6× from dataset alone, then 3.1× from scoring methodology, then another 5.1× from temporal precision requirements—demonstrate how evaluation choices compound to create order-of-magnitude performance variations.

## Recommendations for Transparent Evaluation

Addressing these challenges requires fundamental changes in evaluation practices. First, models should always be evaluated on held-out portions of their training datasets using dataset-matched scoring tools—TUSZ with NEDC, CHB-MIT with their protocols, and private datasets with their clinical standards. Second, papers must report performance across multiple scoring methodologies, acknowledging that different clinical applications require different evaluation approaches. Third, researchers should provide complete operating point curves showing the full sensitivity-false alarm tradeoff space, allowing clinicians to select thresholds appropriate for their use cases. Finally, the community needs to establish minimum reporting standards that include dataset version, evaluation tool version, and complete post-processing parameters to ensure reproducibility.

## Limitations and Scope

Our evaluation focuses on a single model and dataset combination, limiting generalizability to other architectures or datasets. We used the authors' pretrained weights without retraining, preventing us from exploring whether architectural modifications or training strategies could close the performance gap. Our analysis is restricted to seizure detection metrics without considering computational requirements, latency, or other practical deployment constraints. Additionally, TUSZ represents only one clinical context—academic medical center EEG—and performance may differ in community hospitals, ICUs, or ambulatory monitoring scenarios. These limitations emphasize the need for comprehensive evaluation across multiple models, datasets, and clinical contexts.

## Future Directions

This work highlights several critical areas for future research. The field urgently needs standardized evaluation protocols that specify dataset versions, scoring tools, and reporting requirements. Models should be developed with explicit clinical requirements as optimization targets rather than benchmark metrics that may not reflect deployment needs. Real-world validation studies comparing model predictions to clinical outcomes would provide the ultimate test of utility beyond detection metrics. The community should also explore whether ensemble methods, domain adaptation, or clinical fine-tuning can bridge the gap between benchmark and clinical performance. Most importantly, closer collaboration between AI researchers and clinical practitioners is essential to ensure that technical advances translate into patient benefit rather than merely impressive benchmark scores.

