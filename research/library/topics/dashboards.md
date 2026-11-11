# dashboards

- **Do not cram a dashboard with charts.** Dashboards drift into overload; show fewer, linked views and add a short narrative so people with varied visual literacy can follow. Confidence: medium. Sources: B02 p.418-420; B86 p.99
- **Choose lines and bars over gauges, dials and pies.** Gauges, pies and 3D bars are appealing yet hard to compare; fit the primary dashboard on a single screen with minimal scrolling. Confidence: medium. Sources: B86 p.99; B02 p.422-423
- **Derive regions from the user's top questions.** Each panel answers one question (status, progress, next action), and regions that can be empty get the least prominence. Confidence: low. Sources: B25 p.85
- **Show each key figure against a comparison.** Current value next to the prior period and the projection answers whether things are improving; a bare number does not. Confidence: low. Sources: B25 p.87; B26 p.289
- **Keep panels spatially stable for expert work.** Dense professional tools keep tiled, non-overlapping panels in fixed positions and link them so a selection in one updates the others. Confidence: medium. Sources: B21 p.122-123
- **Give summary lists enough items.** A top-three and bottom-three summary proved too thin for monitoring; users wanted longer ranked lists plus alerts. Confidence: low. Sources: B58 p.273
- **Offer one composite score for executives, with components for diagnosis.** A standardized blend of completion, time, errors and satisfaction reads at a glance, while the parts stay one click away. Confidence: medium. Sources: B94 p.271-273
- **Judge anomalies against context, not one fixed limit.** What is unusual depends on time and season, so compute anomaly bands from a rolling window (for example a moving average plus or minus two to four standard deviations) and model known seasonal lows. Confidence: medium. Sources: B61 p.336-342; B12 p.293, 308
- **Keep static thresholds for hard limits.** Error counts, saturation, compliance and service-level limits need fixed thresholds so the system cannot learn to tolerate a breach. Confidence: low. Sources: B12 p.292, 297-298
- **Alert on a pattern of anomalies, not on every spike.** Fire on a count of point anomalies within a window (for example three in a minute) or a change sustained past a duration, to avoid alert floods. Confidence: low. Sources: B12 p.298-302
- **Preview alert settings against history before saving.** Show how many alerts the chosen thresholds would have fired over the last 15 minutes, hour and day. Confidence: low. Sources: B12 p.302, 306-307
- **Monitor model inputs, labels and predictions over time.** Machine-learning dashboards should slice by model version and by week or month so drift shows up. Confidence: low. Sources: B61 p.272-273, 281, 454
