"""
Fuzzy Logic System - Without External Libraries
Input: Crisp values (T, H)
Output: Grade of Membership Function (MF)
"""

class FuzzyLogicSystem:
    def __init__(self):
        # Membership function ranges
        self.temp_range = (0, 55)      # Temperature: 0-55°C
        self.humidity_range = (0, 100)  # Humidity: 0-100%
        
    def triangle_membership(self, x, a, b, c):
        """
        Triangular membership function
        a: left point, b: peak, c: right point
        """
        if x <= a or x >= c:
            return 0.0
        elif a < x <= b:
            return (x - a) / (b - a)
        else:  # b < x < c
            return (c - x) / (c - b)
    
    def trapezoid_membership(self, x, a, b, c, d):
        """
        Trapezoidal membership function
        a: left slope start, b: plateau start
        c: plateau end, d: right slope end
        """
        if x <= a or x >= d:
            return 0.0
        elif a < x <= b:
            return (x - a) / (b - a)
        elif b < x < c:
            return 1.0
        else:  # c <= x < d
            return (d - x) / (d - c)
    
    def calculate_mf_temperature(self, temp):
        """
        Temperature Membership Functions
        D (Cold): 0-20°C
        A (Normal): 15-35°C
        H (Hot): 30-55°C
        """
        mf_d = self.triangle_membership(temp, 0, 10, 20)
        mf_a = self.triangle_membership(temp, 15, 25, 35)
        mf_h = self.triangle_membership(temp, 30, 42.5, 55)
        
        return {
            'D': mf_d,  # Cold
            'A': mf_a,  # Normal
            'H': mf_h   # Hot
        }
    
    def calculate_mf_humidity(self, humidity):
        """
        Humidity Membership Functions
        SK (Very Dry): 0-30%
        K (Dry): 20-60%
        L (Normal): 40-80%
        B (Wet): 70-100%
        SB (Very Wet): 80-100%
        """
        mf_sk = self.triangle_membership(humidity, 0, 15, 30)
        mf_k = self.triangle_membership(humidity, 20, 40, 60)
        mf_l = self.triangle_membership(humidity, 40, 60, 80)
        mf_b = self.triangle_membership(humidity, 70, 85, 100)
        mf_sb = self.triangle_membership(humidity, 80, 90, 100)
        
        return {
            'SK': mf_sk,  # Sangat Kering (Very Dry)
            'K': mf_k,    # Kering (Dry)
            'L': mf_l,    # Lembab (Normal)
            'B': mf_b,    # Basah (Wet)
            'SB': mf_sb   # Sangat Basah (Very Wet)
        }
    
    def calculate_mf_output(self, temp_mf, humidity_mf):
        """
        Output Membership Functions based on Mamdani Rules
        Output: Kipas (Fan Speed)
        Panon (Very Low): 0-15%
        Hompar (Low): 10-40%
        Borah (Medium): 35-65%
        S.Borah (High): 60-100%
        """
        # Simple Mamdani inference rules
        output_mf = {
            'Panon': 0.0,      # Very Low
            'Hompar': 0.0,     # Low
            'Borah': 0.0,      # Medium
            'S.Borah': 0.0     # High
        }
        
        # Rule base (simplified)
        # If Cold and Dry -> Very Low
        output_mf['Panon'] = max(output_mf['Panon'], 
                                 min(temp_mf.get('D', 0), humidity_mf.get('SK', 0)))
        
        # If Normal and Normal -> Low/Medium
        output_mf['Hompar'] = max(output_mf['Hompar'], 
                                  min(temp_mf.get('A', 0), humidity_mf.get('L', 0)))
        
        # If Hot and Normal -> Medium
        output_mf['Borah'] = max(output_mf['Borah'], 
                                 min(temp_mf.get('H', 0), humidity_mf.get('L', 0)))
        
        # If Hot and Wet -> High
        output_mf['S.Borah'] = max(output_mf['S.Borah'], 
                                   min(temp_mf.get('H', 0), humidity_mf.get('SB', 0)))
        
        return output_mf
    
    def defuzzify(self, output_mf):
        """
        Center of Gravity (CoG) Defuzzification
        Converts fuzzy output to crisp value
        """
        # Define center points for each output fuzzy set
        centers = {
            'Panon': 7.5,      # Very Low (0-15)
            'Hompar': 25.0,    # Low (10-40)
            'Borah': 50.0,     # Medium (35-65)
            'S.Borah': 80.0    # High (60-100)
        }
        
        numerator = sum(output_mf[key] * centers[key] for key in output_mf)
        denominator = sum(output_mf.values())
        
        if denominator == 0:
            return 0.0
        
        return numerator / denominator
    
    def process(self, temperature, humidity):
        """
        Main fuzzy logic processing
        Input: temperature (crisp), humidity (crisp)
        Output: grade of membership functions
        """
        # Step 1: Fuzzification
        temp_mf = self.calculate_mf_temperature(temperature)
        humidity_mf = self.calculate_mf_humidity(humidity)
        
        # Step 2: Inference
        output_mf = self.calculate_mf_output(temp_mf, humidity_mf)
        
        # Step 3: Defuzzification
        crisp_output = self.defuzzify(output_mf)
        
        return {
            'temperature_mf': temp_mf,
            'humidity_mf': humidity_mf,
            'output_mf': output_mf,
            'crisp_output': crisp_output
        }


def main():
    """Main program"""
    fuzzy = FuzzyLogicSystem()
    
    print("=" * 70)
    print("FUZZY LOGIC SYSTEM - Temperature & Humidity Control")
    print("=" * 70)
    
    # Example 1
    print("\n--- Input 1 ---")
    temp1 = 42
    humidity1 = 89
    print(f"Temperature: {temp1}°C")
    print(f"Humidity: {humidity1}%")
    
    result1 = fuzzy.process(temp1, humidity1)
    
    print("\nTemperature Membership Functions:")
    for key, value in result1['temperature_mf'].items():
        print(f"  {key}: {value:.4f}")
    
    print("\nHumidity Membership Functions:")
    for key, value in result1['humidity_mf'].items():
        print(f"  {key}: {value:.4f}")
    
    print("\nOutput Membership Functions:")
    for key, value in result1['output_mf'].items():
        print(f"  {key}: {value:.4f}")
    
    print(f"\nCrisp Output (Fan Speed): {result1['crisp_output']:.2f}%")
    
    # Example 2
    print("\n" + "=" * 70)
    print("--- Input 2 ---")
    temp2 = 25
    humidity2 = 60
    print(f"Temperature: {temp2}°C")
    print(f"Humidity: {humidity2}%")
    
    result2 = fuzzy.process(temp2, humidity2)
    
    print("\nTemperature Membership Functions:")
    for key, value in result2['temperature_mf'].items():
        print(f"  {key}: {value:.4f}")
    
    print("\nHumidity Membership Functions:")
    for key, value in result2['humidity_mf'].items():
        print(f"  {key}: {value:.4f}")
    
    print("\nOutput Membership Functions:")
    for key, value in result2['output_mf'].items():
        print(f"  {key}: {value:.4f}")
    
    print(f"\nCrisp Output (Fan Speed): {result2['crisp_output']:.2f}%")
    
    # Interactive mode
    print("\n" + "=" * 70)
    print("Interactive Mode")
    print("=" * 70)
    
    while True:
        try:
            temp = float(input("\nEnter Temperature (°C) [0-55] or -1 to exit: "))
            if temp == -1:
                break
            
            humidity = float(input("Enter Humidity (%) [0-100]: "))
            
            if not (0 <= temp <= 55 and 0 <= humidity <= 100):
                print("⚠️ Values out of range!")
                continue
            
            result = fuzzy.process(temp, humidity)
            
            print(f"\n{'─' * 50}")
            print(f"Input: T={temp}°C, H={humidity}%")
            print(f"{'─' * 50}")
            
            print("\nTemperature MF:")
            for key, val in result['temperature_mf'].items():
                print(f"  {key:4s}: {val:.4f}")
            
            print("\nHumidity MF:")
            for key, val in result['humidity_mf'].items():
                print(f"  {key:4s}: {val:.4f}")
            
            print("\nOutput MF:")
            for key, val in result['output_mf'].items():
                print(f"  {key:10s}: {val:.4f}")
            
            print(f"\n🔧 Fan Speed Output: {result['crisp_output']:.2f}%")
            
        except ValueError:
            print("❌ Invalid input! Please enter numbers.")


if __name__ == "__main__":
    main()
