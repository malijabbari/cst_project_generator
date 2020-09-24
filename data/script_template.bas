Sub Main ()
    ' load project
    OpenFile "$project_path"

    ' run macro
    Macro

    ' export model as dxf
    export_dxf

    ' add macro to history
    AddToHistory "macro", "RunMacro(""macro"")"

    'save
    Save
End Sub

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

$macro_content
