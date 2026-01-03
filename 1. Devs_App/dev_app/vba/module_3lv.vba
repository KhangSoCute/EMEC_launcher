Sub ModifyData()
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    
    Dim ws As Worksheet
    Dim levelCell As Range
    Dim summaryRange As Range
    Dim foundCell As Range
    Dim columnToSetWidth As Range
    
    ' Set the worksheet where you want to modify the data
    Set ws = ThisWorkbook.Worksheets("Sheet1") ' Replace "Sheet1" with the actual sheet name
    
    ' Change values in "Level" column (P:Q)
    Set levelCell = ws.Range("P2:P" & ws.Cells(ws.Rows.Count, "P").End(xlUp).Row)
    For Each cell In levelCell
        Select Case cell.Value
            Case 1
                cell.Value = "NEG"
            Case 2
                cell.Value = "CUT"
            Case 3
                cell.Value = "POS"
        End Select
    Next cell
    
    ' Clear content below "Summary Statistics" (C:K)
    Set summaryRange = ws.Range("C:K")
    Set foundCell = summaryRange.Find("Summary Statistics", LookIn:=xlValues, LookAt:=xlPart)
    If Not foundCell Is Nothing Then
        ws.Range(foundCell.Row & ":" & foundCell.Row + 10).ClearContents
    End If

    ' Clear content below "Action(s)" (C:G)
    Set summaryRange = ws.Range("C:G")
    Set foundCell = summaryRange.Find("Action(s)", LookIn:=xlValues, LookAt:=xlPart)
    If Not foundCell Is Nothing Then
        ws.Range(foundCell.Row & ":" & foundCell.Row).ClearContents
    End If
    
    ' Set the range of the column
    Set columnToSetWidth = ws.Range("K:K") ' Replace "K:K" with your desired column range
    
    ' Set the width of the column in points
    columnToSetWidth.ColumnWidth = 2 ' Replace 100 with your desired width in points
    
    Application.ScreenUpdating = True
    Application.Calculation = xlCalculationAutomatic
End Sub



