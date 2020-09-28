
' -----------------------------------------------------------------------------
' variables
Dim names(), permittivities(), densities(), conductivities()
Dim reds(), greens(), blues()
Dim n_materials, idx As Integer
Dim patient_model, current_object, first_solid, second_solid As String
Dim first_solid_name, second_solid_name as String
Dim componentname, solidname, objectname, treename As String


' -----------------------------------------------------------------------------
' load patient model

With STEP
    .Reset
    .Healing "0"
     .ScaleToUnit "0"
    .FileName "$model_path"
    .Id "1"
    .Version "11.0"
    .ImportToActiveCoordinateSystem "True"
    .Curves "True"
    .ImportAttributes "True"
    .ImportCurveAttributes "True"
    .Read
End With

' -----------------------------------------------------------------------------
' Define materials
names = Array($object_names)
permittivities = Array($permittivities)
densities = Array($densities)
conductivities = Array($conductivities)
reds = Array($reds)
greens = Array($greens)
blues = Array($blues)
n_materials = $n_materials

For idx = 0 To n_materials - 1
    With Material
        .Reset
        .Name names(idx)
        .Folder ""
        .Rho densities(idx)
        .ThermalType "Normal"
        .ThermalConductivity "0"
        .SpecificHeat "0", "J/K/kg"
        .DynamicViscosity "0"
        .Emissivity "0"
        .MetabolicRate "0.0"
        .VoxelConvection "0.0"
        .BloodFlow "0"
        .MechanicsType "Unused"
        .FrqType "all"
        .Type "Normal"
        .MaterialUnit "Frequency", "MHz"
        .MaterialUnit "Geometry", "mm"
        .MaterialUnit "Time", "s"
        .Epsilon permittivities(idx)
        .Mu "1"
        .Sigma conductivities(idx)
        .TanD "0.0"
        .TanDFreq "0.0"
        .TanDGiven "False"
        .TanDModel "ConstTanD"
        .EnableUserConstTanDModelOrderEps "False"
        .ConstTanDModelOrderEps "1"
        .SetElParametricConductivity "False"
        .ReferenceCoordSystem "Global"
        .CoordSystemType "Cartesian"
        .SigmaM "0"
        .TanDM "0.0"
        .TanDMFreq "0.0"
        .TanDMGiven "False"
        .TanDMModel "ConstTanD"
        .EnableUserConstTanDModelOrderMu "False"
        .ConstTanDModelOrderMu "1"
        .SetMagParametricConductivity "False"
        .DispModelEps  "None"
        .DispModelMu "None"
        .DispersiveFittingSchemeEps "Nth Order"
        .MaximalOrderNthModelFitEps "10"
        .ErrorLimitNthModelFitEps "0.1"
        .UseOnlyDataInSimFreqRangeNthModelEps "False"
        .DispersiveFittingSchemeMu "Nth Order"
        .MaximalOrderNthModelFitMu "10"
        .ErrorLimitNthModelFitMu "0.1"
        .UseOnlyDataInSimFreqRangeNthModelMu "False"
        .UseGeneralDispersionEps "False"
        .UseGeneralDispersionMu "False"
        .NLAnisotropy "False"
        .NLAStackingFactor "1"
        .NLADirectionX "1"
        .NLADirectionY "0"
        .NLADirectionZ "0"
        .Colour reds(idx), greens(idx), blues(idx)
        .Wireframe "False"
        .Reflection "False"
        .Allowoutline "True"
        .Transparentoutline "False"
        .Transparency "50"
        .Create
    End With
Next

' -----------------------------------------------------------------------------
' combine subsolids

' do some magic because CST is badly programmed
Resulttree.UpdateTree
Resulttree.RefreshView
Plot.Update

' get the treename of the patient model (not the phased_array)
patient_model = Resulttree.GetFirstChildName("Components")
If InStr(patient_model, "phased_array") > 0 Then
    patient_model = Resulttree.GetNextItemName(patient_model)
End If

' loop through patient_model objects
current_object = Resulttree.GetFirstChildName(patient_model)
While Len(current_object) > 0
    ' combine children
    first_solid = Resulttree.GetFirstChildName(current_object)
    second_solid = Resulttree.GetNextItemName(first_solid)
    Debug.Print second_solid
    While Len(second_solid) > 0

        ' in CST, treename is different from object-name, there doesnt exist
        ' a function to convert this, so it must be done manually.
        ' convert treename of first_solid to object-name
        treename = Split(first_solid, "\", 2)(1)  ' remove "components\"
        componentname = StrReverse( Split( StrReverse(treename) , "\", 2)(1) )
        solidname = StrReverse( Split( StrReverse(treename) , "\", 2)(0) )
        objectname = componentname + ":" + solidname
        objectname = Replace(objectname, "\", "/")  ' replace \ with /
        first_solid_name = objectname

        ' same for second_solid
        treename = Split(second_solid, "\", 2)(1)  ' remove "components\"
        componentname = StrReverse( Split( StrReverse(treename) , "\", 2)(1) )
        solidname = StrReverse( Split( StrReverse(treename) , "\", 2)(0) )
        objectname = componentname + ":" + solidname
        objectname = Replace(objectname, "\", "/")  ' replace \ with /
        second_solid_name = objectname

        ' combine the solids
        Solid.Add first_solid_name, second_solid_name

        ' update tree, as combining the solids will change it
        Resulttree.UpdateTree
        Resulttree.RefreshView

        ' obtain solids again
        '   (second solid should be empty if there is only 1 remaining)
        first_solid = Resulttree.GetFirstChildName(current_object)
        second_solid = Resulttree.GetNextItemName(first_solid)

    Wend

    ' get next object
    current_object = Resulttree.GetNextItemName(current_object)
Wend