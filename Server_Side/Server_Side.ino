//If you use Dragino IoT Mesh Firmware, uncomment below lines.
//For product: LG01. 
#define BAUDRATE 115200
#include <Console.h>
#include <SPI.h>
#include <RH_RF95.h>

// Singleton instance of the radio driver
RH_RF95 rf95;
float frequency = 915.0;

void setup() 
{   
  Bridge.begin(BAUDRATE);
  Console.begin();
  while (!Console) ; // Wait for console port to be available
  Console.println("Start Sketch");
  if (!rf95.init())
    Console.println("init failed");
  // Setup ISM frequency
  rf95.setFrequency(frequency);
  // Setup Power,dBm
  rf95.setTxPower(13);
  
  // Setup Spreading Factor (6 ~ 12)
  rf95.setSpreadingFactor(7);
  
  // Setup BandWidth, option: 7800,10400,15600,20800,31200,41700,62500,125000,250000,500000
  rf95.setSignalBandwidth(125000);
  
  // Setup Coding Rate:5(4/5),6(4/6),7(4/7),8(4/8) 
  rf95.setCodingRate4(5);
  
  Console.print("Listening on frequency: ");
  Console.println(frequency);
}

void loop()
{
  if (rf95.available())
  {
    // Should be a message for us now   
    uint8_t buf[100];
    uint8_t len = sizeof(buf);
    if (rf95.recv(buf, &len))
    {
      //RH_RF95::printBuffer("request: ", buf, len);
      Console.print("got request: ");
      Console.println((char*)buf);
      //Console.print("RSSI: ");
      //Console.println(rf95.lastRssi(), DEC);
      
      // Send a reply
      //uint8_t data[] = "received";
      //rf95.send(data, sizeof(data));
      //rf95.waitPacketSent();
      //Console.println("Sent a reply");

      //forward data to more than one element
      rf95.send(buf, sizeof(buf));
      rf95.waitPacketSent();
      //Console.println("forwarded data!");
    }
    else
    {
      Console.println("recv failed");
    }
  }
}
