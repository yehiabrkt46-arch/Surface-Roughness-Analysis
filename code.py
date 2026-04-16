import numpy as np
import matplotlib.pyplot as plt

def GetData(filename):
    """Load roughness profile CSV with columns: sample_number, X, Y."""
    try:
        data = np.loadtxt(filename, delimiter=',', skiprows=1)
        return data
    except Exception as e:
        print(f"Error loading file: {e}")
        return np.array([])

# --------------------------------
# ### Question 1 Function ###
# --------------------------------
def InspectData(data):
    print("[Q1] Inspecting Data")
    if data.size == 0:
        print("No data loaded.")
        return

    rows, cols = data.shape
    unique_samples = np.unique(data[:, 0]).astype(int)
    print(f"Data contains {rows} rows and {cols} columns.")
    print(f"Unique samples found: {unique_samples}")
    
    while True:
        choice = input("Do you want to print the content of one row? (y/n): ").strip().lower()
        if choice == 'n':
            break
        elif choice == 'y':
            try:
                row_num = int(input("Enter a row number: "))
                if 1 <= row_num <= rows:
                    print(f"Row {row_num}: {data[row_num-1, :]}")
                else:
                    if row_num < 1:
                        diff = 1 - row_num
                    else:
                        diff = row_num - rows
                    print(f"The requested row is {diff} rows out of range.")
            except ValueError:
                print("Invalid input. Please enter an integer.")

# --------------------------------
# ### Question 2 Functions ###
# --------------------------------
def GetSampleRange(data):
    print("[Q2].a Getting Sample Range")
    if data.size == 0:
        return 0, 0
    samples = np.unique(data[:, 0])
    return int(min(samples)), int(max(samples))

def LoadSampleProfile(data):
    print("[Q2].b Loading Sample Profile")
    if data.size == 0:
        return np.array([]), np.array([]), 0
        
    samples = np.unique(data[:, 0])
    while True:
        try:
            sid_input = input(f"Enter Sample ID ({int(min(samples))}-{int(max(samples))}): ")
            sid = int(sid_input)
            if sid in samples:
                mask = data[:, 0] == sid
                sample_data = data[mask]
                return sample_data[:, 1], sample_data[:, 2], sid
            else:
                print("Invalid Sample ID. Please try again.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

# --------------------------------
# ### Question 3 Functions ###
# --------------------------------
def ComputeRa(y_values):
    """
    Takes a 1D array of Y values.
    Calculates Ra (arithmetic mean of absolute deviations from mean).
    Returns Ra value.
    """
    mean_y = np.mean(y_values)
    ra = np.mean(np.abs(y_values - mean_y))
    return ra

def SaveSampleResults(source_filename, sample_id):
    """
    Takes filename and sample_id.
    Loads data, computes Ra.
    Saves to CSV with specific format.
    """
    print(f"[Q3].b Saving Results for Sample {sample_id}")
    
    raw_data = GetData(source_filename)
    if raw_data.size == 0:
        return
    
    mask = raw_data[:, 0] == sample_id
    sample_data = raw_data[mask]
    
    if len(sample_data) == 0:
        print(f"Error: Sample {sample_id} not found.")
        return

    x_values = sample_data[:, 1]
    y_values = sample_data[:, 2]
    ra_value = ComputeRa(y_values)
    
    output_filename = rf"C:\Users\c23042477\Downloads\Sample_{sample_id}.csv"
    
    try:
        with open(output_filename, 'w') as f:
            f.write(f"Sample {sample_id}\n")
            f.write(f"{ra_value:.4f}\n")
            x_str = ",".join(map(str, x_values))
            f.write(x_str + "\n")
            y_str = ",".join(map(str, y_values))
            f.write(y_str + "\n")
            
        print(f"File saved successfully to: {output_filename}")
        
    except Exception as e:
        print(f"Error writing file: {e}")

# --------------------------------
# ### Question 4 Functions ###
# --------------------------------
def PlotProfile(x, y, sample_id, ra):
    """
    Plots Y vs X as a line chart.
    Includes Ra value in the chart label/title.
    """
    print(f"[Q4].a Plotting Profile for Sample {sample_id}")
    plt.figure(figsize=(10, 4))
    plt.plot(x, y, label=f'Sample {sample_id} (Ra={ra:.4f})', color='blue')
    plt.axhline(np.mean(y), color='red', linestyle='--', label='Mean Line')
    plt.title(f"Roughness Profile - Sample {sample_id}")
    plt.xlabel("Position X")
    plt.ylabel("Height Y")
    plt.legend()
    plt.grid(True)
    plt.show()

def CompareRa(sample_ids, ra_values):
    """
    Takes arrays of Sample IDs and Ra values.
    Plots all Ra values in a graph to facilitate comparison.
    """
    print("[Q4].a Comparing Ra Values")
    plt.figure(figsize=(8, 5))
    plt.bar(sample_ids, ra_values, color='purple', alpha=0.7)
    plt.xlabel("Sample ID")
    plt.ylabel("Ra Value")
    plt.title("Comparison of Surface Roughness (Ra) Across Samples")
    plt.xticks(sample_ids)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    for i, v in enumerate(ra_values):
        plt.text(sample_ids[i], v, f"{v:.3f}", ha='center', va='bottom')
        
    plt.show()

# --------------------------------
# ### Question 5 Class ###
# --------------------------------
class RoughnessProfile:
    def __init__(self, data_source, sample_number):
    
        self._SampleNumber = int(sample_number)
        
        # Extract X and Y from the provided data source
        mask = data_source[:, 0] == self._SampleNumber
        if np.sum(mask) == 0:
            print(f"Warning: Sample {self._SampleNumber} not found in provided data.")
            self._X = np.array([])
            self._Y = np.array([])
            self._Ra = 0.0
        else:
            self._X = data_source[mask, 1]
            self._Y = data_source[mask, 2]
            self._Ra = self._ComputeInternalRa()

    def _ComputeInternalRa(self):
        """Internal method to calculate Ra based on current Y values."""
        if len(self._Y) == 0:
            return 0.0
        return np.mean(np.abs(self._Y - np.mean(self._Y)))

    def PrintData(self):
        """Method to print all data stored in the object."""
        print("-" * 30)
        print(f"Class Object: RoughnessProfile")
        print(f"Sample ID   : {self.SampleNumber}")
        print(f"Data Points : {len(self.X)}")
        print(f"Ra Value    : {self.Ra:.4f}")
        print("-" * 30)

    def Plot(self):
        """Method to plot the profile defined by x/y values."""
        if len(self.X) == 0:
            print("No data to plot.")
            return
            
        plt.figure(figsize=(10, 4))
        plt.plot(self.X, self.Y, color='green', label=f'Sample {self.SampleNumber}')
        plt.axhline(np.mean(self.Y), color='orange', linestyle='--', label='Mean')
        plt.title(f"Roughness Profile Object: Sample {self.SampleNumber} (Ra={self.Ra:.4f})")
        plt.xlabel("X Position")
        plt.ylabel("Y Height")
        plt.legend()
        plt.grid(True)
        plt.show()

    # Accessors 
    @property
    def SampleNumber(self):
        return self._SampleNumber

    @property
    def X(self):
        return self._X

    @property
    def Y(self):
        return self._Y

    @property
    def Ra(self):
        return self._Ra

    # Mutator 
    @SampleNumber.setter
    def SampleNumber(self, value):
        if isinstance(value, int):
            print(f"Updating Sample ID from {self._SampleNumber} to {value}")
            self._SampleNumber = value
        else:
            print("Error: Sample Number must be an integer.")


# --------------------------------
# ### Question 1 Body ###
# --------------------------------
FilePath = r"C:\Users\c23042477\Downloads\Data.csv"
RawData = GetData(FilePath)
InspectData(RawData)

# --------------------------------
# ### Question 2 Body ###
# --------------------------------
MinVal, MaxVal = GetSampleRange(RawData)
print(f"Sample IDs range from {MinVal} to {MaxVal}")
# Load profile 
CurrentX, CurrentY, CurrentID = LoadSampleProfile(RawData)

# --------------------------------
# ### Question 3 Body ###
# --------------------------------
print("\n [Q3] Ra Calculation ")
if len(CurrentY) > 0:
    CurrentRa = ComputeRa(CurrentY)
    print(f"Ra for Sample {CurrentID} is {CurrentRa:.4f}")
    SaveSampleResults(FilePath, CurrentID)

# --------------------------------
# ### Question 4 Body ###
# --------------------------------
print("\n [Q4] Plotting and Comparison ")
# 1. Plot Sample 1
Mask1 = RawData[:, 0] == 1
if np.sum(Mask1) > 0:
    Data1 = RawData[Mask1]
    PlotProfile(Data1[:, 1], Data1[:, 2], 1, ComputeRa(Data1[:, 2]))

# 2. Plot Sample 3
Mask3 = RawData[:, 0] == 3
if np.sum(Mask3) > 0:
    Data3 = RawData[Mask3]
    PlotProfile(Data3[:, 1], Data3[:, 2], 3, ComputeRa(Data3[:, 2]))

# 3. Compare All
UniqueIDs = np.unique(RawData[:, 0]).astype(int)
AllRaValues = [ComputeRa(RawData[RawData[:, 0] == sid, 2]) for sid in UniqueIDs]
CompareRa(UniqueIDs, np.array(AllRaValues))

# --------------------------------
# ### Question 5 Body ###
# --------------------------------
print("\n [Q5] Class Implementation ")

# Object 1 using Sample 4
print("\nCreating Object for Sample 4:")
Profile4 = RoughnessProfile(RawData, 4)
Profile4.PrintData()  # Demonstrates print method
Profile4.Plot()       # Demonstrates plot method

# Object 2 using Sample 5
print("\nCreating Object for Sample 5:")
Profile5 = RoughnessProfile(RawData, 5)

# Accessor
print(f"Directly accessing Ra via property for Sample 5: {Profile5.Ra:.4f}")

# Mutator (Changing the ID Label)
Profile5.SampleNumber = 999 
Profile5.PrintData()  

Profile5.Plot()
