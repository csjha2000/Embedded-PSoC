#include "project.h"

#define BAUD_RATE      9.6          // Desired baud rate
#define BIT_DURATION   (1000 / BAUD_RATE)  // Miliseconds per bit for the given baud rate (e.g., 104 ms for 9.6 baud rate)


void transmit(uint8_t byte)
{
    // Start bit (low)
    Pin_1_Write(0);  
    CyDelay(BIT_DURATION);

    
    for (int i = 0; i < 8; i++)
    {
        Pin_1_Write(byte & 0x01); 
        byte >>= 1;               
        CyDelay(BIT_DURATION);  
    }

    // Stop bit (high)
    Pin_1_Write(1); 
    CyDelay(BIT_DURATION);
}

int main(void)
{
    CyGlobalIntEnable; // Enable global interrupts. 

    // Set initial TX pin state to high (idle state for UART)
    Pin_1_Write(1);
    

    // Define the bytes to send
    uint8_t data[] = {0x23, 0x3A, 0xAA}; //0x23, 0x3A, 0xAA
  
    for(;;)
    {
         Pin_1_Write(1);
        CyDelay(BIT_DURATION*10);
        // Continuously transmit each byte
        for (int i = 0; i < 3; i++)
        {
            transmit(data[i]);         
        }
    } 
}

