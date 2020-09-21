Sub Main ()
	' load project
	OpenFile "$project_path"

    ' run macro which loads in the model & changes the material
	AddToHistory("macro", "RunMacro(""macro"")")

	' save project
	Save

End Sub
