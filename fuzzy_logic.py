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
        D (Dingin): 0-30°C
        A (Adem): 10-40°C
        H (Hangat): 30-45°C
        P (Panas): 40-55°C
        SP (Sangat Panas): 45-55°C
        """
        mf_d = self.triangle_membership(temp, 0, 10, 30)
        mf_a = self.triangle_membership(temp, 10, 30, 40)
        mf_h = self.triangle_membership(temp, 30, 40, 45)
        mf_p = self.triangle_membership(temp, 40, 45, 55)
        mf_sp = self.triangle_membership(temp, 45, 50, 55)
        
        return {
            'D': mf_d,      # Dingin (Cold)
            'A': mf_a,      # Adem (Cool)
            'H': mf_h,      # Hangat (Warm)
            'P': mf_p,      # Panas (Hot)
            'SP': mf_sp     # Sangat Panas (Very Hot)
        }
    
    def calculate_mf_humidity(self, humidity):
        """
        Humidity Membership Functions
        SK (Very Dry): 0-30%
        K (Dry): 0-60%
        L (Normal): 30-80%
        B (Wet): 60-90%
        SB (Very Wet): 80-100%
        """
        mf_sk = self.triangle_membership(humidity, 0, 15, 30)
        mf_k = self.triangle_membership(humidity, 0, 30, 60)
        mf_l = self.triangle_membership(humidity, 30, 60, 80)
        mf_b = self.triangle_membership(humidity, 60, 80, 90)
        mf_sb = self.triangle_membership(humidity, 80, 90, 100)
        
        return {
            'SK': mf_sk,    # Sangat Kering (Very Dry)
            'K': mf_k,      # Kering (Dry)
            'L': mf_l,      # Lembab (Normal)
            'B': mf_b,      # Basah (Wet)
            'SB': mf_sb     # Sangat Basah (Very Wet)
        }
    
    def calculate_mf_output(self, temp_mf, humidity_mf):
        """
        Output Membership Functions based on Mamdani Rules
        Output: Kipas (Fan Speed)
        panas (Very Low): 0-15%
        hangat (Low): 10-40%
        basah (Medium): 35-65%
        S.basah (High): 60-100%
        """
        # Simple Mamdani inference rules
        output_mf = {
            'panas': 0.0,       # Very Low
            'hangat': 0.0,      # Low
            'basah': 0.0,       # Medium
            'S.basah': 0.0      # High
        }
        
        # Rule base - Mamdani inference
        # If Dingin and Sangat Kering -> panas (Very Low)
        output_mf['panas'] = max(output_mf['panas'], 
                                 min(temp_mf.get('D', 0), humidity_mf.get('SK', 0)))
        
        # If Adem and Kering -> hangat (Low)
        output_mf['hangat'] = max(output_mf['hangat'], 
                                  min(temp_mf.get('A', 0), humidity_mf.get('K', 0)))
        
        # If Hangat and Normal -> basah (Medium)
        output_mf['basah'] = max(output_mf['basah'], 
                                 min(temp_mf.get('H', 0), humidity_mf.get('L', 0)))
        
        # If Panas and Basah -> S.basah (High)
        output_mf['S.basah'] = max(output_mf['S.basah'], 
                                   min(temp_mf.get('P', 0), humidity_mf.get('B', 0)))
        
        # If Sangat Panas and Sangat Basah -> S.basah (High)
        output_mf['S.basah'] = max(output_mf['S.basah'], 
                                   min(temp_mf.get('SP', 0), humidity_mf.get('SB', 0)))
        
        return output_mf
    
    def defuzzify(self, output_mf):
        """
        Center of Gravity (CoG) Defuzzification
        Converts fuzzy output to crisp value
        """
        # Define center points for each output fuzzy set
        centers = {
            'panas': 7.5,       # Very Low (0-15)
            'hangat': 25.0,     # Low (10-40)
            'basah': 50.0,      # Medium (35-65)
            'S.basah': 80.0     # High (60-100)
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
    
    print("=" * 75)
    print("FUZZY LOGIC SYSTEM - Temperature & Humidity Control")
    print("=" * 75)
    
    # Example 1: Panas
    print("\n--- Input 1: Panas (Hot) ---")
    temp1 = 42
    humidity1 = 89
    print(f"Temperature: {temp1}°C")
    print(f"Humidity: {humidity1}%")
    
    result1 = fuzzy.process(temp1, humidity1)
    
    print("\nTemperature Membership Functions:")
    for key, value in result1['temperature_mf'].items():
        print(f"  {key:4s}: {value:.4f}")
    
    print("\nHumidity Membership Functions:")
    for key, value in result1['humidity_mf'].items():
        print(f"  {key:4s}: {value:.4f}")
    
    print("\nOutput Membership Functions:")
    for key, value in result1['output_mf'].items():
        print(f"  {key:10s}: {value:.4f}")
    
    print(f"\nCrisp Output (Fan Speed): {result1['crisp_output']:.2f}%")
    
    # Example 2: Hangat
    print("\n" + "=" * 75)
    print("--- Input 2: Hangat (Warm) ---")
    temp2 = 35
    humidity2 = 65
    print(f"Temperature: {temp2}°C")
    print(f"Humidity: {humidity2}%")
    
    result2 = fuzzy.process(temp2, humidity2)
    
    print("\nTemperature Membership Functions:")
    for key, value in result2['temperature_mf'].items():
        print(f"  {key:4s}: {value:.4f}")
    
    print("\nHumidity Membership Functions:")
    for key, value in result2['humidity_mf'].items():
        print(f"  {key:4s}: {value:.4f}")
    
    print("\nOutput Membership Functions:")
    for key, value in result2['output_mf'].items():
        print(f"  {key:10s}: {value:.4f}")
    
    print(f"\nCrisp Output (Fan Speed): {result2['crisp_output']:.2f}%")
    
    # Example 3: Sangat Panas
    print("\n" + "=" * 75)
    print("--- Input 3: Sangat Panas (Very Hot) ---")
    temp3 = 50
    humidity3 = 95
    print(f"Temperature: {temp3}°C")
    print(f"Humidity: {humidity3}%")
    
    result3 = fuzzy.process(temp3, humidity3)
    
    print("\nTemperature Membership Functions:")
    for key, value in result3['temperature_mf'].items():
        print(f"  {key:4s}: {value:.4f}")
    
    print("\nHumidity Membership Functions:")
    for key, value in result3['humidity_mf'].items():
        print(f"  {key:4s}: {value:.4f}")
    
    print("\nOutput Membership Functions:")
    for key, value in result3['output_mf'].items():
        print(f"  {key:10s}: {value:.4f}")
    
    print(f"\nCrisp Output (Fan Speed): {result3['crisp_output']:.2f}%")
    
    # Interactive mode
    print("\n" + "=" * 75)
    print("Interactive Mode")
    print("=" * 75)
    
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
            
            print(f"\n{'─' * 60}")
            print(f"Input: T={temp}°C, H={humidity}%")
            print(f"{'─' * 60}")
            
            print("\nTemperature MF:")
            print(f"  D  (Dingin)       : {result['temperature_mf']['D']:.4f}")
            print(f"  A  (Adem)         : {result['temperature_mf']['A']:.4f}")
            print(f"  H  (Hangat)       : {result['temperature_mf']['H']:.4f}")
            print(f"  P  (Panas)        : {result['temperature_mf']['P']:.4f}")
            print(f"  SP (Sangat Panas) : {result['temperature_mf']['SP']:.4f}")
            
            print("\nHumidity MF:")
            print(f"  SK (Sangat Kering): {result['humidity_mf']['SK']:.4f}")
            print(f"  K  (Kering)       : {result['humidity_mf']['K']:.4f}")
            print(f"  L  (Lembab)       : {result['humidity_mf']['L']:.4f}")
            print(f"  B  (Basah)        : {result['humidity_mf']['B']:.4f}")
            print(f"  SB (Sangat Basah) : {result['humidity_mf']['SB']:.4f}")
            
            print("\nOutput MF:")
            for key, val in result['output_mf'].items():
                print(f"  {key:10s}: {val:.4f}")
            
            print(f"\n🔧 Fan Speed Output: {result['crisp_output']:.2f}%")
            
        except ValueError:
            print("❌ Invalid input! Please enter numbers.")


if __name__ == "__main__":
    main()
