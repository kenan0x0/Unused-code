        team_workbook = Workbook()
        sheet = team_workbook.active
        
        # Update the default sheet name to Info
        sheet.title = "Info"

        # Add the default cell content
        sheet["A2"] = "Please refer to Sample page for format"
        sheet["A1"] = "Insait Coach"
        sheet["A3"] = "Required"
        sheet["D3"] = "Optional"
        sheet["A4"] = "Player ID"
        sheet["B4"] = "Name"
        sheet["C4"] = "Gender"
        sheet["D4"] = "Date of Birth"

        # Add the merges to the default style
        sheet.merge_cells("A1:F1")
        sheet.merge_cells("A2:F2")
        sheet.merge_cells("A3:C3")
        sheet.merge_cells("D3:F3")

        # Applying styles to the cells in the excel file
        a1 = sheet["A1"]
        font_a1 = Font(
            size=22,
            bold=True
        )
        align_a1 = Alignment(
            horizontal="center"
        )

        player_counter = 0
        for i in range(len(players_in_chosen_team)):
            i += 5
            sheet[f"A{i}"] = players_in_chosen_team[player_counter][0]
            sheet[f"B{i}"] = players_in_chosen_team[player_counter][1]
            sheet[f"C{i}"] = players_in_chosen_team[player_counter][2]
            sheet[f"D{i}"] = str(players_in_chosen_team[player_counter][3]).replace('-','/')
            player_counter += 1

        team_workbook.save(filename=f"/app/platform/app/static/team-excels/{chosen_team}.xlsx")
