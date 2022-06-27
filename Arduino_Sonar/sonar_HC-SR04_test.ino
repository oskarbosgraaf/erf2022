#define trigPin1 3
#define echoPin1 2
#define trigPin2 5
#define echoPin2 4
#define trigPin3 6
#define echoPin3 7

long duration, distance, SensorRight, SensorFront, SensorLeft;

void setup()
{
Serial.begin (9600);
pinMode(trigPin1, OUTPUT);
pinMode(echoPin1, INPUT);
pinMode(trigPin2, OUTPUT);
pinMode(echoPin2, INPUT);
pinMode(trigPin3, OUTPUT);
pinMode(echoPin3, INPUT);
}

void loop() {
SonarSensor(trigPin1, echoPin1);
SensorRight = distance;
SonarSensor(trigPin2, echoPin2);
SensorFront = distance;
SonarSensor(trigPin3, echoPin3);
SensorLeft = distance;

Serial.print(SensorLeft);
Serial.print(" - ");
Serial.print(SensorFront);
Serial.print(" - ");
Serial.println(SensorRight);
}


void SonarSensor(int trigPin,int echoPin)
{
digitalWrite(trigPin, LOW);
delayMicroseconds(2);
digitalWrite(trigPin, HIGH);
delayMicroseconds(10);
digitalWrite(trigPin, LOW);
duration = pulseIn(echoPin, HIGH);
distance = (duration/2) / 29.1;

}
