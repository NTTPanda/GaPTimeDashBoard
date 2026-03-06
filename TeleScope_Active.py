
import pandas as pd

# Load CSV
df = pd.read_csv("Data.csv")

# Convert since/till to datetime (your format is DD-MM-YYYY HH:MM)
df['since'] = pd.to_datetime(df['since'], dayfirst=True, errors='coerce')
df['till'] = pd.to_datetime(df['till'], dayfirst=True, errors='coerce')



# Drop rows where datetime failed to parse
df = df.dropna(subset=['since', 'till'])

# Sort globally
df = df.sort_values(['node_id', 'since'])

# Extract only the date (YYYY-MM-DD)
df['date'] = df['since'].dt.date

gaps_output = []
summary_output = []

# Process node by node
for node, node_group in df.groupby('node_id'):

    # Process date by date inside node
    for date, group in node_group.groupby('date'):

        group = group.sort_values('since')
        total_minutes = 0

        for i in range(len(group) - 1):

            end = group.iloc[i]['till']
            next_start = group.iloc[i + 1]['since']

            # Calculate gap
            gap = next_start - end

            if gap.total_seconds() > 0:
                minutes = gap.total_seconds() / 60
                hours = minutes / 60
                total_minutes += minutes

                # Clean formatting (remove unnecessary "0 days")
                clean_gap = str(gap).replace("0 days ", "")

                gaps_output.append({
                    "node_id": node,
                    "date": date,
                    "gap_start": end,
                    "gap_end": next_start,
                    "gap_duration": clean_gap,
                    "gap_minutes": round(minutes, 2),
                    "gap_hours": round(hours, 2)
                })

        # Summary per node per day
        summary_output.append({
            "node_id": node,
            "date": date,
            "total_free_hours": round(total_minutes / 60, 2)
        })

# Convert results to DataFrames
gaps_df = pd.DataFrame(gaps_output)
summary_df = pd.DataFrame(summary_output)

# Save result CSVs
gaps_df.to_csv("free_time_gaps_nodewise.csv", index=False)
summary_df.to_csv("free_time_summary_nodewise.csv", index=False)

print("Files created:")
print(" - free_time_gaps_nodewise.csv")
print(" - free_time_summary_nodewise.csv")