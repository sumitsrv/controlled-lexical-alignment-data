from pathlib import Path

def read_dialogue_csv(file_path):
    """Read dialogue from CSV file and return list of (speaker, utterance) tuples."""
    utterances = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                # Alternate between S1 and S2
                speaker = f"S{((i - 1) % 2) + 1}"
                utterance = parts[1].strip()
                utterances.append((speaker, utterance))
    return utterances

def generate_paired_html(dialogue1_path, dialogue2_path, output_path, order):
    """Generate HTML table snippet with two dialogues side by side in specified order."""
    dialogue1 = read_dialogue_csv(dialogue1_path)
    dialogue2 = read_dialogue_csv(dialogue2_path)
    
    if order == "1-2":
        first_dialogue = dialogue1
        second_dialogue = dialogue2
        first_label = "Dialogue A"
        second_label = "Dialogue B"
    else:  # order == "2-1"
        first_dialogue = dialogue2
        second_dialogue = dialogue1
        first_label = "Dialogue B"
        second_label = "Dialogue A"
    
    # Build table rows with side-by-side dialogues
    max_turns = max(len(first_dialogue), len(second_dialogue))
    table_rows = []
    
    for i in range(max_turns):
        # First dialogue column
        if i < len(first_dialogue):
            speaker1, utterance1 = first_dialogue[i]
            cell1 = f'\t\t\t<td width="50" style="border-right:1px solid white; font-size:16px; color:black; padding: 0 5px;"><b>{speaker1}:</b></td>\n\t\t\t<td width="250" style="font-size:16px; color:black; padding: 0 3px;">{utterance1}</td>'
        else:
            cell1 = '\t\t\t<td width="50" style="border-right:1px solid white; font-size:16px; color:black; padding: 0 5px;"></td>\n\t\t\t<td width="250" style="font-size:16px; color:black; padding: 0 3px;"></td>'
        
        # Second dialogue column
        if i < len(second_dialogue):
            speaker2, utterance2 = second_dialogue[i]
            cell2 = f'\t\t\t<td width="50" style="border-left:2px solid black; border-right:1px solid white; font-size:16px; color:black; padding: 0 3px;"><b>{speaker2}:</b></td>\n\t\t\t<td width="250" style="font-size:16px; color:black; padding: 0 3px;">{utterance2}</td>'
        else:
            cell2 = '\t\t\t<td width="50" style="border-left:2px solid black; border-right:1px solid white; font-size:16px; color:black; padding: 0 3px;"></td>\n\t\t\t<td width="250" style="font-size:16px; color:black; padding: 0 3px;"></td>'
        
        table_rows.append(f"\t\t<tr>\n{cell1}\n{cell2}\n\t\t</tr>")
    
    # Generate instructions and table without full HTML page
    html_content = f"""<span style="font-size:16px;">Rank the following dialogues from the best (1) to the worst (2)&nbsp;based on the relevance and coherence of the responses </span><span style="color:#000000;"><span style="font-size:16px;">by S2</span></span><span style="font-size:16px;">.<br>
<br>
Relevance: The appropriateness of responses to immediate conversational context, i.e., the previous utterance of Speaker 1 (S1)<br>
Coherence: The maintenance of thematic consistency and logical progression with respect to the full dialogue.</span><br>
<br>
&nbsp;
<table style="width:900px; font-size:16px; color:black;" border="1">
\t<tbody>
\t\t<tr>
\t\t\t<th colspan="2">{first_label}</th>
\t\t\t<th style="border-left:2px solid black" colspan="2">{second_label}</th>
\t\t</tr>
\t\t<tr>
\t\t</tr>
{chr(10).join(table_rows)}
\t</tbody>
</table>"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

def main():
    base_dir = Path(__file__).parent
    output_dir = base_dir / "htmls"
    output_dir.mkdir(exist_ok=True)
    
    # Define pairs: (model, weight_0, weight_other, theme)
    pairs = [
        ("bb3b", "0", "75", "culture2"),
        ("bb3b", "0", "25", "culture"),
        ("llama", "0", "750", "health"),
        ("llama", "0", "1000", "environment"),
        ("phi", "0", "3500", "culture"),
        ("phi", "0", "3250", "education"),
    ]
    
    # Create log file
    log_lines = ["HTML Generation Summary", "=" * 80, ""]
    
    for model, weight_0, weight_other, theme in pairs:
        file_0 = base_dir / f"{model}_{theme}_{weight_0}.csv"
        file_other = base_dir / f"{model}_{theme}_{weight_other}.csv"
        
        if not file_0.exists():
            print(f"Warning: {file_0} does not exist. Skipping.")
            log_lines.append(f"Warning: {file_0.name} does not exist. Skipping.")
            continue
        if not file_other.exists():
            print(f"Warning: {file_other} does not exist. Skipping.")
            log_lines.append(f"Warning: {file_other.name} does not exist. Skipping.")
            continue
        
        # Generate order 1-2
        output_1_2 = output_dir / f"{model}_{theme}_order1-2.html"
        generate_paired_html(file_0, file_other, output_1_2, "1-2")
        print(f"Generated: {output_1_2.name}")
        log_lines.append(f"File: {output_1_2.name}")
        log_lines.append(f"  Dialogue A: {file_0.name} (weight={weight_0})")
        log_lines.append(f"  Dialogue B: {file_other.name} (weight={weight_other})")
        log_lines.append("")
        
        # Generate order 2-1
        output_2_1 = output_dir / f"{model}_{theme}_order2-1.html"
        generate_paired_html(file_0, file_other, output_2_1, "2-1")
        print(f"Generated: {output_2_1.name}")
        log_lines.append(f"File: {output_2_1.name}")
        log_lines.append(f"  Dialogue A: {file_other.name} (weight={weight_other})")
        log_lines.append(f"  Dialogue B: {file_0.name} (weight={weight_0})")
        log_lines.append("")
    
    # Write log file
    log_file = output_dir / "generation_log.txt"
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_lines))
    print(f"\nLog file created: {log_file.name}")

if __name__ == "__main__":
    main()
