import read_files_S101
import compare_files_S101


S101_FC_filepath = "..\\..\\compared_documents\\S-101_FC_1.1.0_20230202.xml"
S101_DCEG_filepath = "..\\..\\compared_documents\\S-101 Annex A_DCEG Edition 1.1.0_Final_Clean.docx"


dict_FC_S101 = read_files_S101.read_FC_S101(S101_FC_filepath)
dict_DCEG_S101 = read_files_S101.read_DCEG_S101(S101_DCEG_filepath)

(omission_SimpleAttributes_DCEG,
omission_SimpleAttributes_definition_DCEG,
inconsistent_SimpleAttributes_definition,
omission_SimpleAttributes_alias_DCEG,
inconsistent_SimpleAttributes_alias,
inconsistent_SimpleAttributes_type,
ommission_SimpleAttributes_enum_DCEG,
ommission_SimpleAttributes_enum_FC,
inconsitent_SimpleAttributes_enum_label,
inconsitent_SimpleAttributes_enum_def,
inconsistent_SimpleAttributes_code_FC) = compare_files_S101.compare_FC_DCEG_S101_SimpleAttributes(dict_FC_S101, dict_DCEG_S101)

(omission_ComplexAttributes_DCEG,
 inconsistent_ComplexAttributes_DCEG_title,
 inconsistent_ComplexAttributes_definition,
 omission_ComplexAttributes_definition_DCEG,
 inconsistent_ComplexAttributes_alias,
 omission_ComplexAttributes_alias_DCEG,
 inconsistent_ComplexAttributes_subAttributes) = compare_files_S101.compare_FC_DCEG_S101_ComplexAttributes(dict_FC_S101, dict_DCEG_S101)

(omission_Roles_DCEG,
 inconsistent_Roles_DCEG_title,
 inconsistent_Roles_definition,
 omission_Roles_definition_DCEG) = compare_files_S101.compare_FC_DCEG_S101_Roles(dict_FC_S101, dict_DCEG_S101)

(omission_FeatureAssociations_DCEG,
 inconsistent_FeatureAssociations_DCEG_title,
 inconsistent_FeatureAssociations_definition,
 omission_FeatureAssociations_definition_DCEG,
 inconsistent_FeatureAssociations_roles) = compare_files_S101.compare_FC_DCEG_S101_FeatureAssociations(dict_FC_S101, dict_DCEG_S101)

(omission_InformationTypes_DCEG,
 inconsistent_InformationTypes_DCEG_title,
 inconsistent_InformationTypes_definition,
 omission_InformationTypes_definition_DCEG,
 inconsistent_InformationTypes_attributes,
 inconsistent_InformationTypes_multiplicity) = compare_files_S101.compare_FC_DCEG_S101_InformationTypes(dict_FC_S101, dict_DCEG_S101)

(omission_FeatureTypes_DCEG,
 inconsistent_FeatureTypes_DCEG_title,
 inconsistent_FeatureTypes_definition,
 omission_FeatureTypes_definition_DCEG,
 inconsistent_FeatureTypes_alias,
 omission_FeatureTypes_alias_DCEG,
 inconsistent_FeatureTypes_attributes,
 inconsistent_FeatureTypes_multiplicity,
 FeatureTypes_multiplicity_error,
 inconsistent_FeatureTypes_permittedValues) = compare_files_S101.compare_FC_DCEG_S101_FeatureTypes(dict_FC_S101, dict_DCEG_S101)