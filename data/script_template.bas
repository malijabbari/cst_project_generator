Sub Main ()
	' load project
	OpenFile "$project_path"

    ' run macro which loads in the model & changes the material
    '   also manually add it to history because CST sucks and its code is full
    '   of bugs
    RunMacro("macro")
	AddToHistory("macro", "RunMacro(""macro"")")

	' export patient model as 2d dxf format
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

	' save project
	Save

End Sub
