# 🌾 FarmProfit AI

A Streamlit hackathon prototype for:

**Farmer inputs → external weather data → ML yield/price prediction → cost estimation → risk scoring → profit optimization → what-if simulation**

## 1. Install

Create/activate your Python environment and run:

```bash
pip install -r requirements.txt
```

## 2. Run

```bash
streamlit run app.py
```

The app opens in your browser.

## 3. What is real vs demo?

### Real API
The app automatically geocodes the farm location and retrieves a 7-day weather forecast from Open-Meteo.

### Demo components
The yield and price models are trained on synthetic data generated inside `app.py`.
The market-price adjustment is also a demo table.

This is intentional: the app gives you a working end-to-end prototype first. For the final hackathon submission, replace synthetic data with real historical agricultural data.

### Disease image model
The crop photo upload is included in the UI, but the current prototype uses a temporary disease-severity slider. Do NOT claim that the current version diagnoses disease from the image.

## 4. Recommended hackathon upgrades

1. Replace synthetic yield training data with historical crop-yield data.
2. Replace demo prices with validated mandi/market data.
3. Train a crop-disease image classifier.
4. Add historical weather features.
5. Add SHAP explanations for the ML models.
6. Add a proper optimization layer with budget and water constraints.
7. Add Tamil/vernacular UI.
8. Add farmer-friendly explanations instead of raw ML scores.

## 5. Suggested architecture

```text
             Farmer
                |
        Small set of inputs
                |
      +---------+----------+
      |                    |
 Weather API          Agriculture DB
      |                    |
      +---------+----------+
                |
          Feature Builder
                |
       +--------+--------+
       |        |        |
    Yield     Price    Risk/CV
     ML        ML       Model
       |        |        |
       +--------+--------+
                |
         Cost Estimator
                |
        Profit Optimizer
                |
      Best Crop + Profit
       + Risk + Reason
                |
          What-if Tool
```

## 6. Important judging point

Do not present this as:

> "AI predicts which crop is best."

Present it as:

> **"A constrained agricultural decision-intelligence system that maximizes expected farm profit under weather, water, soil, disease and budget uncertainty."**

That framing makes the ML and optimization components much clearer.
