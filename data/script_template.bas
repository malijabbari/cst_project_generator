Sub Main ()
    ' create log
	Open "$log_path" For Output As #1
	tab = Chr(9)

	' load project
	Print #1, "loading project..."
	OpenFile "$project_path"
	Print #1, tab + "...done"


	' run macro which loads in the model & changes the material
	'   also manually add it to history because CST sucks and its code is full
	'   of bugs
	Print #1, "running macro..."
	RunScript("$macro_path")
	Print #1, tab + "...done"

	Print #1, "adding macro to history..."
	AddToHistory("macro", "RunMacro(""macro"")")
	Print #1, tab + "...done"

	' export patient model as 2d dxf format
	Print #1, "exporting model as 2d dxf..."
	WCS.ActivateWCS "local"
	With WCS
		.SetNormal "0", "1", "0"
		.SetUVector "0", "0", "1"
		.ActivateWCS "local"
	End With
	WCS.ActivateWCS "global"
	With DXF
		.Reset
		.FileName "$model2d_path"
		.Write
	End With
	Print #1, tab + "...done"

	'save project
	Print #1, "saving project..."
	Save
	Print #1, tab + "...done"

	' close log file
	Close #1

End Sub
