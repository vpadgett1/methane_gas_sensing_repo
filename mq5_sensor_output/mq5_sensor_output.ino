float sensor=A0;
float gas_value;

void setup(){
  pinMode(sensor,INPUT);
  Serial.begin(9600);
}

void loop(){
  //Serial.println("MQ5 Heating Up!");
  delay(20000); // allow the MQ5 to warm up
  gas_value=analogRead(sensor);
  Serial.print(gas_value);
  Serial.println(" ppm");
  delay(40000);
}
