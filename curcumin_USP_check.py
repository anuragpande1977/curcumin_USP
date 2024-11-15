import pandas as pd
import streamlit as st

# Updated reference data with serial numbers
REFERENCE_DATA = {
    "SL No": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "BDMC (Assay)": [2.67, 2.74, 2.71, 2.6, 2.84, 2.75, 2.55, 2.5, 2.56, 2.93],
    "Curcumin (Assay)": [75.74, 75.26, 75.32, 75.96, 75.49, 75.27, 76.26, 75.03, 75.17, 79.88],
    "DMC (Assay)": [16.12, 16.4, 16.3, 15.9, 16.37, 16.94, 16.51, 16.88, 16.9, 15.18],
    "Total Curcuminoids (Assay)": [95.04, 95.29, 95.18, 95.29, 95.43, 95.75, 95.78, 95.08, 95.18, 95.22]
}

def load_reference_data():
    # Convert embedded reference data into a DataFrame
    df = pd.DataFrame(REFERENCE_DATA)
    
    # Calculate ratios for the dataset
    df['Curcumin_to_DMC'] = df['Curcumin (Assay)'] / df['DMC (Assay)']
    df['Curcumin_to_BDMC'] = df['Curcumin (Assay)'] / df['BDMC (Assay)']
    df['DMC_to_BDMC'] = df['DMC (Assay)'] / df['BDMC (Assay)']
    
    return df

def calculate_statistics(df):
    # Calculate mean and standard deviation for each component and each ratio
    return {
        'Curcumin_mean': df['Curcumin (Assay)'].mean(),
        'Curcumin_std': df['Curcumin (Assay)'].std(),
        'DMC_mean': df['DMC (Assay)'].mean(),
        'DMC_std': df['DMC (Assay)'].std(),
        'BDMC_mean': df['BDMC (Assay)'].mean(),
        'BDMC_std': df['BDMC (Assay)'].std(),
        'Curcumin_to_DMC_mean': df['Curcumin_to_DMC'].mean(),
        'Curcumin_to_DMC_std': df['Curcumin_to_DMC'].std(),
        'Curcumin_to_BDMC_mean': df['Curcumin_to_BDMC'].mean(),
        'Curcumin_to_BDMC_std': df['Curcumin_to_BDMC'].std(),
        'DMC_to_BDMC_mean': df['DMC_to_BDMC'].mean(),
        'DMC_to_BDMC_std': df['DMC_to_BDMC'].std()
    }

def check_sample_conformity(sample, reference_stats):
    # Calculate z-scores for each component in the sample
    z_scores = {
        'Curcumin': (sample['Curcumin'] - reference_stats['Curcumin_mean']) / reference_stats['Curcumin_std'],
        'DMC': (sample['DMC'] - reference_stats['DMC_mean']) / reference_stats['DMC_std'],
        'BDMC': (sample['BDMC'] - reference_stats['BDMC_mean']) / reference_stats['BDMC_std'],
        'Curcumin_to_DMC': (sample['Curcumin'] / sample['DMC'] - reference_stats['Curcumin_to_DMC_mean']) / reference_stats['Curcumin_to_DMC_std'],
        'Curcumin_to_BDMC': (sample['Curcumin'] / sample['BDMC'] - reference_stats['Curcumin_to_BDMC_mean']) / reference_stats['Curcumin_to_BDMC_std'],
        'DMC_to_BDMC': (sample['DMC'] / sample['BDMC'] - reference_stats['DMC_to_BDMC_mean']) / reference_stats['DMC_to_BDMC_std']
    }
    
    # Check if all Z-scores for components are within range
    is_within_z = all(abs(z_scores[key]) <= 2 for key in ['Curcumin', 'DMC', 'BDMC'])
    
    # Check if all Z-scores for ratios are within range
    is_within_ratios = all(abs(z_scores[key]) <= 2 for key in ['Curcumin_to_DMC', 'Curcumin_to_BDMC', 'DMC_to_BDMC'])
    
    # Final decision: Conformity requires both component and ratio Z-scores to be within range
    if is_within_z and is_within_ratios:
        result = "Conforms to natural variation"
    else:
        result = "Outlier - Does not conform to natural variation"
    
    return result, z_scores

# Streamlit App
def main():
    st.title("Curcumin Test Batch Analysis")

    # Load reference data
    reference_df = load_reference_data()
    reference_stats = calculate_statistics(reference_df)
    
    # Input test batch values
    st.header("Enter Test Batch Results")
    curcumin = st.number_input("Curcumin (Assay)", min_value=0.0, max_value=100.0, value=0.0, step=0.01)
    dmc = st.number_input("DMC (Assay)", min_value=0.0, max_value=100.0, value=0.0, step=0.01)
    bdmc = st.number_input("BDMC (Assay)", min_value=0.0, max_value=100.0, value=0.0, step=0.01)
    
    if st.button("Analyze"):
        sample_input = {'Curcumin': curcumin, 'DMC': dmc, 'BDMC': bdmc}
        
        # Check conformity
        result, z_scores = check_sample_conformity(sample_input, reference_stats)
        
        # Display results
        st.header("Results")
        st.write(" - **Conformity Result**: ", result)
        st.write(" - **Z-scores**: ")
        st.json(z_scores)

# Run the Streamlit app
if __name__ == "__main__":
    main()
