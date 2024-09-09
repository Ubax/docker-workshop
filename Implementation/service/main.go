package main

import (
    "context"
    "encoding/json"
    "fmt"
    "log"
    "net/http"
    "os"
    "time"

    "github.com/joho/godotenv"
    "go.mongodb.org/mongo-driver/bson"
    "go.mongodb.org/mongo-driver/mongo"
    "go.mongodb.org/mongo-driver/mongo/options"
)

// Define the report structure
type Report struct {
    Name string  `json:"name" bson:"name"`
    Q1   float64 `json:"q1" bson:"q1"`
    Q2   float64 `json:"q2" bson:"q2"`
    Q3   float64 `json:"q3" bson:"q3"`
    Q4   float64 `json:"q4" bson:"q4"`
}

// MongoDB client
var client *mongo.Client

// Connect to MongoDB
func connectToMongoDB() *mongo.Client {
    mongoURI := os.Getenv("MONGODB_URI")
    if mongoURI == "" {
        log.Fatal("MONGODB_URI is not set")
    }

    ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
    defer cancel()

    clientOptions := options.Client().ApplyURI(mongoURI)
    client, err := mongo.Connect(ctx, clientOptions)
    if err != nil {
        log.Fatalf("Failed to connect to MongoDB: %v", err)
    }

    // Check the connection
    err = client.Ping(ctx, nil)
    if err != nil {
        log.Fatalf("Failed to ping MongoDB: %v", err)
    }

    fmt.Println("Connected to MongoDB!")
    return client
}

// Handler for the /report endpoint
func reportHandler(w http.ResponseWriter, r *http.Request) {
    dbName := os.Getenv("DB_NAME")
    collection := client.Database(dbName).Collection("quarterly-results") // Replace with your DB and collection name

    // Fetch reports from MongoDB
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()

    cursor, err := collection.Find(ctx, bson.M{})
    if err != nil {
        http.Error(w, "Failed to fetch reports", http.StatusInternalServerError)
        return
    }
    defer cursor.Close(ctx)

    var reports []Report
    if err := cursor.All(ctx, &reports); err != nil {
        http.Error(w, "Failed to decode reports", http.StatusInternalServerError)
        return
    }

    // Set the content type to application/json
    w.Header().Set("Content-Type", "application/json")
    
    // Encode the report array into JSON and write the response
    json.NewEncoder(w).Encode(reports)
}

func main() {
    if err := godotenv.Load(); err != nil {
		log.Println("No .env file found")
	}
    port := os.Getenv("PORT")
    if port == "" {
        port = "5001"
    }

    // Connect to MongoDB
    client = connectToMongoDB()

    // Set up the /report route and its handler
    http.HandleFunc("/report", reportHandler)

    // Start the server on the specified port
    addr := fmt.Sprintf(":%s", port)
    fmt.Printf("Server running on port %s\n", port)
    http.ListenAndServe(addr, nil)
}
