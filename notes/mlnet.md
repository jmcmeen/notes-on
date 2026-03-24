# Introduction to ML.NET

## Table of Contents

1. [What is ML.NET?](#what-is-mlnet)
2. [Installation](#installation)
3. [Core Concepts](#core-concepts)
4. [Data Loading](#data-loading)
5. [Data Transformation](#data-transformation)
6. [Classification](#classification)
7. [Regression](#regression)
8. [Clustering](#clustering)
9. [Model Evaluation](#model-evaluation)
10. [Model Consumption](#model-consumption)
11. [AutoML](#automl)
12. [Saving and Loading Models](#saving-and-loading-models)
13. [Practice Exercises](#practice-exercises)
14. [Summary](#summary)

---

## What is ML.NET?

ML.NET is Microsoft's open-source, cross-platform machine learning framework designed for .NET developers. It allows you to build, train, and deploy custom machine learning models using C# or F# without requiring deep expertise in ML frameworks like TensorFlow or PyTorch.

Key features of ML.NET include:
- **Native .NET integration**: Build ML models entirely in C# or F# with no Python dependency
- **Wide algorithm support**: Classification, regression, clustering, anomaly detection, recommendation, ranking, and forecasting
- **AutoML**: Automatically explore and select the best model and hyperparameters
- **ONNX interoperability**: Import and export models in ONNX format for cross-platform use
- **TensorFlow and PyTorch integration**: Consume pre-trained deep learning models via ONNX
- **Production-ready**: Designed for scalable, high-performance inference in .NET applications

---

## Installation

ML.NET is distributed via NuGet packages. Install the core package and any task-specific packages you need.

```csharp
// Install via .NET CLI
// dotnet add package Microsoft.ML
// dotnet add package Microsoft.ML.AutoML
// dotnet add package Microsoft.ML.TensorFlow

// Or via NuGet Package Manager Console in Visual Studio
// Install-Package Microsoft.ML
// Install-Package Microsoft.ML.AutoML
```

```csharp
// Verify installation in a new console project
using Microsoft.ML;

// Create an MLContext, the starting point for all ML.NET operations
var mlContext = new MLContext();
Console.WriteLine("ML.NET is installed and ready.");
```

Common NuGet packages and their purposes:
- `Microsoft.ML` -- Core library with data loading, transforms, and trainers
- `Microsoft.ML.AutoML` -- Automated machine learning capabilities
- `Microsoft.ML.TensorFlow` -- TensorFlow model integration
- `Microsoft.ML.OnnxRuntime` -- ONNX model inference
- `Microsoft.ML.ImageAnalytics` -- Image processing transforms
- `Microsoft.ML.Recommender` -- Matrix factorization for recommendations
- `Microsoft.ML.TimeSeries` -- Time series forecasting and anomaly detection

---

## Core Concepts

ML.NET revolves around a few fundamental abstractions that work together to form a pipeline-based workflow.

### MLContext

```csharp
// MLContext is the entry point for all ML.NET operations
// It provides factories for data loading, transforms, trainers, and model operations
var mlContext = new MLContext(seed: 42); // seed for reproducibility

// MLContext contains catalogs for different operations
// mlContext.Data         -> data loading and manipulation
// mlContext.Transforms   -> feature engineering and preprocessing
// mlContext.BinaryClassification -> binary classification trainers
// mlContext.MulticlassClassification -> multiclass trainers
// mlContext.Regression   -> regression trainers
// mlContext.Clustering   -> clustering trainers
// mlContext.Model        -> model saving and loading
```

### IDataView

```csharp
// IDataView is ML.NET's core data abstraction, similar to a DataFrame
// It is lazy-evaluated, immutable, and supports schema-aware columnar data

// Define a data class with column attributes
public class HousingData
{
    [LoadColumn(0)]  // Map to CSV column index
    public float Size { get; set; }

    [LoadColumn(1)]
    public float Bedrooms { get; set; }

    [LoadColumn(2)]
    public float Price { get; set; }
}

// Load data into an IDataView
IDataView dataView = mlContext.Data.LoadFromTextFile<HousingData>(
    path: "housing.csv",
    hasHeader: true,
    separatorChar: ','
);

// Preview data (materialize a small portion for inspection)
var preview = dataView.Preview(maxRows: 5);
foreach (var row in preview.RowView)
{
    Console.WriteLine(string.Join(", ", row.Values));
}
```

### Pipelines, Transformers, and Trainers

```csharp
// A pipeline chains together transforms and a trainer
// Transforms: preprocess and featurize data (IEstimator -> ITransformer)
// Trainers: learn patterns from data (produce a trained model)

// Build a pipeline step by step
var pipeline = mlContext.Transforms.Concatenate(
        "Features",             // output column name
        "Size", "Bedrooms"      // input columns to combine
    )
    .Append(mlContext.Transforms.NormalizeMinMax("Features")) // normalize features
    .Append(mlContext.Regression.Trainers.Sdca(              // append a trainer
        labelColumnName: "Price",
        featureColumnName: "Features"
    ));

// Train the model by fitting the pipeline to data
ITransformer model = pipeline.Fit(dataView);
// model is now a trained transformer that can make predictions
```

---

## Data Loading

ML.NET supports loading data from various sources into IDataView.

### Loading from CSV

```csharp
// Load from a CSV file with automatic column mapping
public class SentimentData
{
    [LoadColumn(0)]
    public string Text { get; set; }

    [LoadColumn(1)]
    public bool Label { get; set; }
}

IDataView data = mlContext.Data.LoadFromTextFile<SentimentData>(
    path: "sentiment.csv",
    hasHeader: true,
    separatorChar: ','
);
```

SQL databases are also supported via `DatabaseLoader` and `DatabaseSource` with `System.Data.SqlClient`.

### Loading from In-Memory Collections

```csharp
// Load data from an in-memory list of objects
var inMemoryData = new List<HousingData>
{
    new HousingData { Size = 1200, Bedrooms = 2, Price = 250000 },
    new HousingData { Size = 1800, Bedrooms = 3, Price = 375000 },
    new HousingData { Size = 2400, Bedrooms = 4, Price = 480000 },
    new HousingData { Size = 900,  Bedrooms = 1, Price = 180000 },
    new HousingData { Size = 3200, Bedrooms = 5, Price = 620000 }
};

// Convert the list to an IDataView
IDataView inMemView = mlContext.Data.LoadFromEnumerable(inMemoryData);
```

### Splitting Data

```csharp
// Split data into training and test sets
var split = mlContext.Data.TrainTestSplit(
    data,
    testFraction: 0.2,    // 20% for testing
    seed: 42               // reproducibility
);

IDataView trainData = split.TrainSet;
IDataView testData = split.TestSet;
```

---

## Data Transformation

Transforms preprocess raw data into a format suitable for machine learning trainers.

### Concatenating Features

```csharp
// Combine multiple columns into a single Features vector
var concatPipeline = mlContext.Transforms.Concatenate(
    "Features",                        // output column
    "Size", "Bedrooms", "YearBuilt"    // input columns to merge
);
```

### Normalization

```csharp
// Normalize numeric features to a common scale
// MinMax normalization scales values to [0, 1]
var normPipeline = mlContext.Transforms.NormalizeMinMax("Features");

// MeanVariance normalization (zero mean, unit variance)
var meanVarPipeline = mlContext.Transforms.NormalizeMeanVariance("Features");

// Log normalization for skewed distributions
var logNormPipeline = mlContext.Transforms.NormalizeLogMeanVariance("Features");
```

### Encoding Categorical Data

```csharp
// One-hot encode a categorical string column
var encodePipeline = mlContext.Transforms.Categorical.OneHotEncoding(
    outputColumnName: "CityEncoded",
    inputColumnName: "City"
);

// Hash encoding for high-cardinality categorical features
var hashPipeline = mlContext.Transforms.Categorical.OneHotHashEncoding(
    outputColumnName: "ZipEncoded",
    inputColumnName: "ZipCode",
    numberOfBits: 10  // controls the hash space size
);

// Convert a label string to a key type (required for multiclass)
var labelPipeline = mlContext.Transforms.Conversion.MapValueToKey("Label");
```

### Text Featurization

```csharp
// Transform raw text into a numeric feature vector
// Includes tokenization, stop word removal, n-grams, and TF-IDF
var textPipeline = mlContext.Transforms.Text.FeaturizeText(
    outputColumnName: "TextFeatures",
    inputColumnName: "ReviewText"
);

// Custom text processing pipeline with finer control
var customTextPipeline = mlContext.Transforms.Text.NormalizeText("NormText", "ReviewText")
    .Append(mlContext.Transforms.Text.TokenizeIntoWords("Tokens", "NormText"))
    .Append(mlContext.Transforms.Text.RemoveDefaultStopWords("CleanTokens", "Tokens"))
    .Append(mlContext.Transforms.Text.ProduceNgrams("Ngrams", "CleanTokens",
        ngramLength: 2,    // bigrams
        useAllLengths: true // include unigrams too
    ))
    .Append(mlContext.Transforms.Text.FeaturizeText("TextFeatures", "ReviewText"));
```

### Handling Missing Values

```csharp
// Replace missing values with a computed or default value
var missingPipeline = mlContext.Transforms.ReplaceMissingValues(
    "Size", replacementMode: MissingValueReplacingEstimator.ReplacementMode.Mean
);
// ReplacementMode options: Mean, Minimum, Maximum, DefaultValue
```

---

## Classification

### Binary Classification

```csharp
// Binary classification: predict one of two outcomes (true/false, yes/no)
public class SpamInput
{
    [LoadColumn(0)]
    public string Message { get; set; }

    [LoadColumn(1)]
    public bool IsSpam { get; set; }
}

public class SpamPrediction
{
    [ColumnName("PredictedLabel")]
    public bool IsSpam { get; set; }

    public float Probability { get; set; }  // confidence score
    public float Score { get; set; }        // raw score
}

// Build the full training pipeline
var spamPipeline = mlContext.Transforms.Text.FeaturizeText(
        "Features", "Message"                    // convert text to features
    )
    .Append(mlContext.BinaryClassification.Trainers.SdcaLogisticRegression(
        labelColumnName: "IsSpam",
        featureColumnName: "Features"
    ));

// Train the model
var spamData = mlContext.Data.LoadFromTextFile<SpamInput>("spam.csv", hasHeader: true);
var spamSplit = mlContext.Data.TrainTestSplit(spamData, testFraction: 0.2);
ITransformer spamModel = spamPipeline.Fit(spamSplit.TrainSet);

// Evaluate on the test set
var spamPredictions = spamModel.Transform(spamSplit.TestSet);
var spamMetrics = mlContext.BinaryClassification.Evaluate(spamPredictions, "IsSpam");
Console.WriteLine($"Accuracy: {spamMetrics.Accuracy:F4}");
Console.WriteLine($"AUC:      {spamMetrics.AreaUnderRocCurve:F4}");
Console.WriteLine($"F1 Score: {spamMetrics.F1Score:F4}");
```

### Multiclass Classification

```csharp
// Multiclass classification: predict one of many categories
public class IrisData
{
    [LoadColumn(0)] public float SepalLength { get; set; }
    [LoadColumn(1)] public float SepalWidth { get; set; }
    [LoadColumn(2)] public float PetalLength { get; set; }
    [LoadColumn(3)] public float PetalWidth { get; set; }
    [LoadColumn(4)] public string Species { get; set; }
}

public class IrisPrediction
{
    [ColumnName("PredictedLabel")]
    public string Species { get; set; }
}

// Pipeline: map label to key, concatenate features, train, map key back to label
var irisPipeline = mlContext.Transforms.Conversion.MapValueToKey("Label", "Species")
    .Append(mlContext.Transforms.Concatenate("Features",
        "SepalLength", "SepalWidth", "PetalLength", "PetalWidth"))
    .Append(mlContext.MulticlassClassification.Trainers.SdcaMaximumEntropy(
        labelColumnName: "Label",
        featureColumnName: "Features"))
    .Append(mlContext.Transforms.Conversion.MapKeyToValue(
        "PredictedLabel", "PredictedLabel"));  // convert predicted key back to string

// Train and evaluate
var irisData = mlContext.Data.LoadFromTextFile<IrisData>("iris.csv", hasHeader: true);
var irisSplit = mlContext.Data.TrainTestSplit(irisData, testFraction: 0.2);
var irisModel = irisPipeline.Fit(irisSplit.TrainSet);

var irisPreds = irisModel.Transform(irisSplit.TestSet);
var irisMetrics = mlContext.MulticlassClassification.Evaluate(irisPreds, "Label");
Console.WriteLine($"Macro Accuracy: {irisMetrics.MacroAccuracy:F4}");
Console.WriteLine($"Micro Accuracy: {irisMetrics.MicroAccuracy:F4}");
Console.WriteLine($"Log Loss:       {irisMetrics.LogLoss:F4}");
```

---

## Regression

```csharp
// Regression: predict a continuous numeric value
public class TaxiTrip
{
    [LoadColumn(0)] public float PassengerCount { get; set; }
    [LoadColumn(1)] public float TripDistance { get; set; }
    [LoadColumn(2)] public float TripDuration { get; set; }
    [LoadColumn(3)] public float FareAmount { get; set; }  // label to predict
}

public class FarePrediction
{
    [ColumnName("Score")]
    public float FareAmount { get; set; }
}

// Build regression pipeline with FastTree (gradient boosted trees)
var farePipeline = mlContext.Transforms.Concatenate(
        "Features",
        "PassengerCount", "TripDistance", "TripDuration"
    )
    .Append(mlContext.Transforms.NormalizeMinMax("Features"))
    .Append(mlContext.Regression.Trainers.FastTree(
        labelColumnName: "FareAmount",
        featureColumnName: "Features",
        numberOfLeaves: 20,        // tree complexity
        numberOfTrees: 100,        // number of boosting iterations
        minimumExampleCountPerLeaf: 10
    ));

// Train and evaluate
var taxiData = mlContext.Data.LoadFromTextFile<TaxiTrip>("taxi.csv", hasHeader: true);
var taxiSplit = mlContext.Data.TrainTestSplit(taxiData, testFraction: 0.2);
var fareModel = farePipeline.Fit(taxiSplit.TrainSet);

var farePreds = fareModel.Transform(taxiSplit.TestSet);
var fareMetrics = mlContext.Regression.Evaluate(farePreds, "FareAmount");
Console.WriteLine($"R-Squared: {fareMetrics.RSquared:F4}");         // 1.0 is perfect
Console.WriteLine($"MAE:       {fareMetrics.MeanAbsoluteError:F4}");
Console.WriteLine($"RMSE:      {fareMetrics.RootMeanSquaredError:F4}");

// Available regression trainers:
// mlContext.Regression.Trainers.Sdca()              -- stochastic dual coordinate ascent
// mlContext.Regression.Trainers.FastTree()           -- gradient boosted trees
// mlContext.Regression.Trainers.FastForest()         -- random forest
// mlContext.Regression.Trainers.LbfgsPoissonRegression() -- Poisson regression
// mlContext.Regression.Trainers.OnlineGradientDescent()  -- SGD-based
```

---

## Clustering

```csharp
// Clustering: group data points into clusters without labels
public class CustomerData
{
    [LoadColumn(0)] public float AnnualIncome { get; set; }
    [LoadColumn(1)] public float SpendingScore { get; set; }
    [LoadColumn(2)] public float Age { get; set; }
}

public class ClusterPrediction
{
    [ColumnName("PredictedLabel")]
    public uint ClusterId { get; set; }    // assigned cluster

    [ColumnName("Score")]
    public float[] Distances { get; set; } // distance to each cluster centroid
}

// Build clustering pipeline with KMeans
var clusterPipeline = mlContext.Transforms.Concatenate(
        "Features", "AnnualIncome", "SpendingScore", "Age"
    )
    .Append(mlContext.Transforms.NormalizeMinMax("Features")) // important for distance-based
    .Append(mlContext.Clustering.Trainers.KMeans(
        featureColumnName: "Features",
        numberOfClusters: 4   // specify number of clusters
    ));

// Train the clustering model
var custData = mlContext.Data.LoadFromTextFile<CustomerData>("customers.csv", hasHeader: true);
var clusterModel = clusterPipeline.Fit(custData);

// Predict cluster assignments
var clusterPreds = clusterModel.Transform(custData);
var predResults = mlContext.Data.CreateEnumerable<ClusterPrediction>(clusterPreds, reuseRowObject: false);

foreach (var pred in predResults.Take(5))
{
    Console.WriteLine($"Cluster: {pred.ClusterId}, Distances: [{string.Join(", ", pred.Distances.Select(d => d.ToString("F2")))}]");
}

// Evaluate clustering quality
var clusterMetrics = mlContext.Clustering.Evaluate(clusterPreds);
Console.WriteLine($"Average Distance: {clusterMetrics.AverageDistance:F4}");
Console.WriteLine($"Davies-Bouldin Index: {clusterMetrics.DaviesBouldinIndex:F4}");
```

---

## Model Evaluation

```csharp
// Evaluation metrics for each task type

// --- Binary Classification Metrics ---
var binMetrics = mlContext.BinaryClassification.Evaluate(predictions, "Label");
Console.WriteLine($"Accuracy:  {binMetrics.Accuracy:F4}");
Console.WriteLine($"AUC-ROC:   {binMetrics.AreaUnderRocCurve:F4}");
Console.WriteLine($"AUC-PR:    {binMetrics.AreaUnderPrecisionRecallCurve:F4}");
Console.WriteLine($"F1 Score:  {binMetrics.F1Score:F4}");
Console.WriteLine($"Precision: {binMetrics.PositivePrecision:F4}");
Console.WriteLine($"Recall:    {binMetrics.PositiveRecall:F4}");

// --- Multiclass Classification Metrics ---
var mcMetrics = mlContext.MulticlassClassification.Evaluate(predictions, "Label");
Console.WriteLine($"Macro Accuracy:  {mcMetrics.MacroAccuracy:F4}");
Console.WriteLine($"Micro Accuracy:  {mcMetrics.MicroAccuracy:F4}");
Console.WriteLine($"Log Loss:        {mcMetrics.LogLoss:F4}");
Console.WriteLine($"Confusion Matrix:\n{mcMetrics.ConfusionMatrix.GetFormattedConfusionTable()}");

// --- Regression Metrics ---
var regMetrics = mlContext.Regression.Evaluate(predictions, "Label");
Console.WriteLine($"R-Squared: {regMetrics.RSquared:F4}");
Console.WriteLine($"MAE:       {regMetrics.MeanAbsoluteError:F4}");
Console.WriteLine($"MSE:       {regMetrics.MeanSquaredError:F4}");
Console.WriteLine($"RMSE:      {regMetrics.RootMeanSquaredError:F4}");

// --- Cross-Validation ---
// Evaluate model stability across multiple folds
var cvResults = mlContext.Regression.CrossValidate(
    data: taxiData,
    estimator: farePipeline,
    numberOfFolds: 5,
    labelColumnName: "FareAmount"
);

// Aggregate cross-validation results
var avgR2 = cvResults.Average(r => r.Metrics.RSquared);
var avgRmse = cvResults.Average(r => r.Metrics.RootMeanSquaredError);
Console.WriteLine($"Cross-Val Avg R2:   {avgR2:F4}");
Console.WriteLine($"Cross-Val Avg RMSE: {avgRmse:F4}");
```

---

## Model Consumption

```csharp
// PredictionEngine creates single-prediction wrappers around trained models
// Suitable for lightweight or on-demand inference scenarios

// Create a PredictionEngine from the trained model
var predEngine = mlContext.Model.CreatePredictionEngine<TaxiTrip, FarePrediction>(fareModel);

// Make a single prediction
var sampleTrip = new TaxiTrip
{
    PassengerCount = 2,
    TripDistance = 3.5f,
    TripDuration = 15.0f
};

var farePred = predEngine.Predict(sampleTrip);
Console.WriteLine($"Predicted fare: ${farePred.FareAmount:F2}");

// PredictionEngine for classification
var spamEngine = mlContext.Model.CreatePredictionEngine<SpamInput, SpamPrediction>(spamModel);

var testMessage = new SpamInput { Message = "Congratulations! You won a free prize!" };
var spamResult = spamEngine.Predict(testMessage);
Console.WriteLine($"Is Spam: {spamResult.IsSpam}, Probability: {spamResult.Probability:F4}");
```

For production scenarios, use `PredictionEnginePool` from `Microsoft.Extensions.ML` for thread-safe, pooled inference in ASP.NET Core applications.

---

## AutoML

```csharp
// AutoML automatically experiments with multiple algorithms and hyperparameters
// to find the best model for your data

// Requires: dotnet add package Microsoft.ML.AutoML

using Microsoft.ML.AutoML;

// Set up an AutoML experiment for regression
var experiment = mlContext.Auto().CreateRegressionExperiment(
    maxExperimentTimeInSeconds: 120  // time budget in seconds
);

// Run the experiment on your data
var autoResult = experiment.Execute(
    trainData: taxiSplit.TrainSet,
    labelColumnName: "FareAmount"
);

// Inspect the best model found
Console.WriteLine($"Best Trainer: {autoResult.BestRun.TrainerName}");
Console.WriteLine($"Best R2:      {autoResult.BestRun.ValidationMetrics.RSquared:F4}");
Console.WriteLine($"Best RMSE:    {autoResult.BestRun.ValidationMetrics.RootMeanSquaredError:F4}");

// Use the best model for predictions
ITransformer bestModel = autoResult.BestRun.Model;
var bestEngine = mlContext.Model.CreatePredictionEngine<TaxiTrip, FarePrediction>(bestModel);
var autoFare = bestEngine.Predict(sampleTrip);
Console.WriteLine($"AutoML predicted fare: ${autoFare.FareAmount:F2}");
```

AutoML also supports `CreateBinaryClassificationExperiment` and `CreateMulticlassClassificationExperiment`. Access `RunDetails` on the result to view a leaderboard of all attempted algorithms sorted by accuracy.

---

## Saving and Loading Models

```csharp
// Save a trained model to a ZIP file for later use
var modelPath = "trained_model.zip";

// Save the model along with its data schema
mlContext.Model.Save(fareModel, taxiSplit.TrainSet.Schema, modelPath);
Console.WriteLine($"Model saved to {modelPath}");

// Load the model back from disk
ITransformer loadedModel = mlContext.Model.Load(modelPath, out var modelSchema);

// Create a prediction engine from the loaded model
var loadedEngine = mlContext.Model.CreatePredictionEngine<TaxiTrip, FarePrediction>(loadedModel);
var loadedPred = loadedEngine.Predict(sampleTrip);
Console.WriteLine($"Loaded model prediction: ${loadedPred.FareAmount:F2}");
```

Models can also be exported to ONNX format using `Microsoft.ML.OnnxConverter` for cross-platform deployment in Python, Java, and JavaScript runtimes.

---

## Practice Exercises

### Exercise 1: Sentiment Analysis Pipeline
Build a binary classifier to predict positive/negative sentiment from product reviews.

```csharp
// 1. Define input and output classes
// 2. Load review data from CSV
// 3. Build a pipeline: FeaturizeText -> SdcaLogisticRegression
// 4. Train, evaluate (Accuracy, F1, AUC), and print the confusion matrix
// 5. Test with custom review strings using PredictionEngine
```

### Exercise 2: House Price Prediction
Build a regression model to predict house prices from features like size, location, and age.

```csharp
// 1. Define a HouseData class with numeric and categorical features
// 2. Load data and split into train/test sets
// 3. Pipeline: OneHotEncode("Neighborhood") -> Concatenate -> Normalize -> FastTree
// 4. Evaluate with R-Squared and RMSE
// 5. Run 5-fold cross-validation and compare scores
```

### Exercise 3: AutoML Comparison
Use AutoML to find the best algorithm, then compare it against a manually chosen trainer.

```csharp
// 1. Pick a dataset (classification or regression)
// 2. Run AutoML with a 2-minute time budget
// 3. Record the best trainer and its metrics
// 4. Manually build a pipeline with a different trainer
// 5. Compare metrics side-by-side and discuss tradeoffs
```

---

## Summary

ML.NET provides a complete machine learning workflow within the .NET ecosystem:
- **MLContext** is the entry point for all operations
- **IDataView** provides lazy, immutable, columnar data representation
- **Pipelines** chain together data transforms and trainers into a reproducible workflow
- **Transforms** handle normalization, encoding, text featurization, and missing values
- **Trainers** cover classification, regression, clustering, and more
- **AutoML** automates algorithm selection and hyperparameter tuning
- **PredictionEngine** and **PredictionEnginePool** serve predictions in apps and APIs
- Models can be saved as ZIP files or exported to ONNX for cross-platform use

---

## Next Steps

- Explore **anomaly detection** with `mlContext.AnomalyDetection.Trainers`
- Build a **recommendation engine** using matrix factorization (`Microsoft.ML.Recommender`)
- Try **time series forecasting** with SSA or ARIMA via `Microsoft.ML.TimeSeries`
- Integrate pre-trained **TensorFlow** or **ONNX** deep learning models
- Deploy models in **ASP.NET Core** web APIs with `PredictionEnginePool`
- Use **Model Builder** in Visual Studio for a guided, UI-driven ML workflow

---

## Additional Resources

- [ML.NET Official Documentation](https://learn.microsoft.com/en-us/dotnet/machine-learning/)
- [ML.NET GitHub Repository](https://github.com/dotnet/machinelearning)
- [ML.NET Samples](https://github.com/dotnet/machinelearning-samples)
- [ML.NET API Reference](https://learn.microsoft.com/en-us/dotnet/api/microsoft.ml)
- [AutoML Documentation](https://learn.microsoft.com/en-us/dotnet/machine-learning/automate-training-with-model-builder)
- [Model Builder Guide](https://learn.microsoft.com/en-us/dotnet/machine-learning/automate-training-with-model-builder)
