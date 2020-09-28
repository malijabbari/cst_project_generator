' -----------------------------------------------------------------------------
Sub Main ()
    ' load project
    OpenFile "$project_path"

    ' run history-type commands and add these to history
    history_commands
    AddToHistory "script - history commands", $history_inline

    ' export model as 2D dxf
    export_dxf

    ' run simulation
    RunSolver

    ' update results tree (dumb dumb CST doesn't know what to export otherwise)
    Resulttree.UpdateTree

    ' export e-fields
    export_efields

    'save
    Save
End Sub


' -----------------------------------------------------------------------------
Sub history_commands
    $history
End Sub


' -----------------------------------------------------------------------------
Sub export_dxf
    ' activate wcs, move it to xyz=0,0,0 and align with xz plane
    With WCS
    	.ActivateWCS "local"
    	.AlignWCSWithGlobalCoordinates
        .SetNormal "0", "1", "0"
        .SetUVector "0", "0", "1"
    End With

    ' export wcs 2d view as dxf
    With DXF
        .Reset
        .FileName "../../../model2d.dxf"
        .Write
    End With

    ' reactivate global coordinates
    WCS.ActivateWCS "global"
End Sub


' -----------------------------------------------------------------------------
Sub export_efields
    e_field = Resulttree.GetFirstChildName("2D/3D Results\E-Field")
    idx = 0
	While Len(e_field) > 0
		SelectTreeItem (e_field)
		ReportInformation e_field_name

		With ASCIIExport
	        .Reset
	        .FileName "../../../e-field " + format(idx, "00") + ".csv"
	        .Mode "FixedWidth"
	        .SetfileType "csv"
	        .SetCsvSeparator ";"
	        .StepX 1.5
	        .StepY 1.5
	        .StepZ 1.5
	        .Execute
	    End With

		e_field = Resulttree.GetNextItemName(e_field)
		idx = idx + 1

        ' do some magic, because CST is badly programmed
		Resulttree.UpdateTree
	    Resulttree.RefreshView
		Plot.Update
	Wend
End Sub