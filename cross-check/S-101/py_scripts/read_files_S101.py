# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 14:31:46 2023

@author: hchonavel
"""

import xml.etree.ElementTree as ET
import zipfile
import numpy as np


def parse_xml(xml_filepath):
    tree = ET.parse(xml_filepath)
    return(tree)


# Fonction permettant de lire le FC S-101    
def read_FC_S101(S101_FC_filepath):
    dict_FC_S101 = dict()
    
    tree = parse_xml(S101_FC_filepath)
    root = tree.getroot()
    
    xmlns = root.tag.split('S100_FC_FeatureCatalogue')[0]
    
    # Lecture de la partie S100_FC_SimpleAttributes
    dict_SimpleAttributes = dict()
    
    S100_FC_SimpleAttributes = root.find(xmlns+"S100_FC_SimpleAttributes") 
    for S100_FC_SimpleAttribute in S100_FC_SimpleAttributes.findall(xmlns+"S100_FC_SimpleAttribute"):
        dict_SimpleAttribute = dict()
        
        name = S100_FC_SimpleAttribute.find(xmlns+'name').text
        definition = S100_FC_SimpleAttribute.find(xmlns+'definition').text
        code = S100_FC_SimpleAttribute.find(xmlns+'code').text
        valueType = S100_FC_SimpleAttribute.find(xmlns+'valueType').text
        
        dict_SimpleAttribute['name'] = name
        dict_SimpleAttribute['definition'] = definition
        dict_SimpleAttribute['code'] = code
        dict_SimpleAttribute['valueType'] = valueType
        
        if not len(S100_FC_SimpleAttribute.findall(xmlns+'alias'))==0:
            alias_lst = [x.text for x in S100_FC_SimpleAttribute.findall(xmlns+'alias')]
            dict_SimpleAttribute['alias'] = alias_lst

        if valueType == "enumeration":
            dict_listedValues = dict()
            listedValues = S100_FC_SimpleAttribute.find(xmlns+'listedValues')
            for listedValue in listedValues.findall(xmlns+'listedValue'):
                dict_listedValue = dict()
                enum_label = listedValue.find(xmlns+'label').text
                enum_definition = listedValue.find(xmlns+'definition').text
                enum_code = listedValue.find(xmlns+'code').text
                
                dict_listedValue['label'] = enum_label
                dict_listedValue['definition'] = enum_definition
                dict_listedValue['code'] = enum_code
                
                dict_listedValues[enum_code] = dict_listedValue
                
            dict_SimpleAttribute['listedValues'] = dict_listedValues
            
        dict_SimpleAttributes[name] = dict_SimpleAttribute
    
    dict_FC_S101['SimpleAttributes'] = dict_SimpleAttributes
    
    # Lecture de la partie S100_FC_ComplexAttributes
    dict_ComplexAttributes = dict()
    
    S100_FC_ComplexAttributes = root.find(xmlns+"S100_FC_ComplexAttributes") 
    for S100_FC_ComplexAttribute in S100_FC_ComplexAttributes.findall(xmlns+"S100_FC_ComplexAttribute"):
        dict_ComplexAttribute = dict()
        
        name = S100_FC_ComplexAttribute.find(xmlns+'name').text
        definition = S100_FC_ComplexAttribute.find(xmlns+'definition').text
        code = S100_FC_ComplexAttribute.find(xmlns+'code').text
        
        dict_ComplexAttribute['name'] = name
        dict_ComplexAttribute['definition'] = definition
        dict_ComplexAttribute['code'] = code
        
        if not len(S100_FC_ComplexAttribute.findall(xmlns+'alias'))==0:
            alias_lst = [x.text for x in S100_FC_ComplexAttribute.findall(xmlns+'alias')]
            dict_ComplexAttribute['alias'] = alias_lst
        
        dict_subAttributes = dict()
        
        for subAttributeBinding in S100_FC_ComplexAttribute.findall(xmlns+'subAttributeBinding'):
            dict_subAttribute = dict()
            subAttrib_code = subAttributeBinding.find(xmlns+'attribute').get('ref')
            mul_lower = subAttributeBinding.find(xmlns+'multiplicity').find(xmlns.replace('S100FC','S100Base')+'lower').text
            mul_upper = subAttributeBinding.find(xmlns+'multiplicity').find(xmlns.replace('S100FC','S100Base')+'upper').text
            if mul_upper is None:
                if subAttributeBinding.find(xmlns+'multiplicity').find(xmlns.replace('S100FC','S100Base')+'upper').get('infinite') == 'true':
                    mul_upper = '*'
                
            multiplicity = mul_lower+','+mul_upper

            dict_subAttribute['code'] = subAttrib_code
            dict_subAttribute['multiplicity'] = multiplicity

            if not subAttributeBinding.find(xmlns+'permittedValues') is None:
                permittedValues = [x.text for x in subAttributeBinding.find(xmlns+'permittedValues').findall(xmlns+'value')]
                dict_subAttribute['permittedValues'] = permittedValues
            
            dict_subAttributes[subAttrib_code] = dict_subAttribute
        
        dict_ComplexAttribute['subAttributes'] = dict_subAttributes
        
        dict_ComplexAttributes[name] = dict_ComplexAttribute
        
    dict_FC_S101['ComplexAttributes'] = dict_ComplexAttributes

    # Lecture de la partie S100_FC_Roles
    dict_Roles = dict()
    S100_FC_Roles = root.find(xmlns+"S100_FC_Roles") 
    for S100_FC_Role in S100_FC_Roles.findall(xmlns+"S100_FC_Role"):
        dict_Role = dict()
        
        name = S100_FC_Role.find(xmlns+'name').text
        definition = S100_FC_Role.find(xmlns+'definition').text
        code = S100_FC_Role.find(xmlns+'code').text

        dict_Role['name'] = name
        dict_Role['definition'] = definition
        dict_Role['code'] = code
        
        dict_Roles[name] = dict_Role
    
    dict_FC_S101['Roles'] = dict_Roles

    # Lecture de la partie S100_FC_FeatureAssociations
    dict_FeatureAssociations = dict()
    S100_FC_FeatureAssociations = root.find(xmlns+"S100_FC_FeatureAssociations") 
    for S100_FC_FeatureAssociation in S100_FC_FeatureAssociations.findall(xmlns+"S100_FC_FeatureAssociation"):
        dict_FeatureAssociation = dict()
        
        name = S100_FC_FeatureAssociation.find(xmlns+'name').text
        definition = S100_FC_FeatureAssociation.find(xmlns+'definition').text
        code = S100_FC_FeatureAssociation.find(xmlns+'code').text

        dict_FeatureAssociation['name'] = name
        dict_FeatureAssociation['definition'] = definition
        dict_FeatureAssociation['code'] = code
        
        role_lst = list()
        for role in S100_FC_FeatureAssociation.findall(xmlns+'role'):
            role_lst.append(role.get('ref'))
        dict_FeatureAssociation['roles'] = role_lst
        
        dict_FeatureAssociations[name] = dict_FeatureAssociation
        
    dict_FC_S101['FeatureAssociations'] = dict_FeatureAssociations

    # Lecture de la partie S100_FC_InformationTypes
    dict_InformationTypes = dict()
    S100_FC_InformationTypes = root.find(xmlns+"S100_FC_InformationTypes") 
    for S100_FC_InformationType in S100_FC_InformationTypes.findall(xmlns+"S100_FC_InformationType"):
        dict_InformationType = dict()
        
        name = S100_FC_InformationType.find(xmlns+'name').text
        definition = S100_FC_InformationType.find(xmlns+'definition').text
        code = S100_FC_InformationType.find(xmlns+'code').text

        dict_InformationType['name'] = name
        dict_InformationType['definition'] = definition
        dict_InformationType['code'] = code
        
        if not len(S100_FC_InformationType.findall(xmlns+'alias'))==0:
            alias_lst = [x.text for x in S100_FC_InformationType.findall(xmlns+'alias')]
            dict_InformationType['alias'] = alias_lst
        
        dict_attributes = dict()
        for attributeBinding in S100_FC_InformationType.findall(xmlns+'attributeBinding'):
            dict_attribute = dict()
            attrib_code = attributeBinding.find(xmlns+'attribute').get('ref')
            mul_lower = attributeBinding.find(xmlns+'multiplicity').find(xmlns.replace('S100FC','S100Base')+'lower').text
            mul_upper = attributeBinding.find(xmlns+'multiplicity').find(xmlns.replace('S100FC','S100Base')+'upper').text
            if mul_upper is None:
                if attributeBinding.find(xmlns+'multiplicity').find(xmlns.replace('S100FC','S100Base')+'upper').get('infinite') == 'true':
                    mul_upper = '*'
                
            multiplicity = mul_lower+','+mul_upper

            dict_attribute['code'] = attrib_code
            dict_attribute['multiplicity'] = multiplicity

            dict_attributes[attrib_code] = dict_attribute
        
        dict_InformationType['attributes'] = dict_attributes

        dict_InformationTypes[name] = dict_InformationType
    
    dict_FC_S101['InformationTypes'] = dict_InformationTypes 

    # Lecture de la partie S100_FC_FeatureTypes
    dict_FeatureTypes = dict()
    S100_FC_FeatureTypes = root.find(xmlns+"S100_FC_FeatureTypes") 
    for S100_FC_FeatureType in S100_FC_FeatureTypes.findall(xmlns+"S100_FC_FeatureType"):
        dict_FeatureType = dict()
        
        name = S100_FC_FeatureType.find(xmlns+'name').text
        definition = S100_FC_FeatureType.find(xmlns+'definition').text
        code = S100_FC_FeatureType.find(xmlns+'code').text

        dict_FeatureType['name'] = name
        dict_FeatureType['definition'] = definition
        dict_FeatureType['code'] = code
        
        if not len(S100_FC_FeatureType.findall(xmlns+'alias'))==0:
            alias_lst = [x.text for x in S100_FC_FeatureType.findall(xmlns+'alias')]
            dict_FeatureType['alias'] = alias_lst
        
        dict_attributes = dict()
        for attributeBinding in S100_FC_FeatureType.findall(xmlns+'attributeBinding'):
            dict_attribute = dict()
            attrib_code = attributeBinding.find(xmlns+'attribute').get('ref')
            mul_lower = attributeBinding.find(xmlns+'multiplicity').find(xmlns.replace('S100FC','S100Base')+'lower').text
            mul_upper = attributeBinding.find(xmlns+'multiplicity').find(xmlns.replace('S100FC','S100Base')+'upper').text
            if mul_upper is None:
                if attributeBinding.find(xmlns+'multiplicity').find(xmlns.replace('S100FC','S100Base')+'upper').get('infinite') == 'true':
                    mul_upper = '*'
                
            multiplicity = mul_lower+','+mul_upper

            dict_attribute['code'] = attrib_code
            dict_attribute['multiplicity'] = multiplicity

            if not attributeBinding.find(xmlns+'permittedValues') is None:
                permittedValues = [x.text for x in attributeBinding.find(xmlns+'permittedValues').findall(xmlns+'value')]
                dict_attribute['permittedValues'] = permittedValues
            
            dict_attributes[attrib_code] = dict_attribute
        
        dict_FeatureType['attributes'] = dict_attributes
        
        dict_FeatureTypes[name] = dict_FeatureType
    
    dict_FC_S101['FeatureTypes'] = dict_FeatureTypes        
    
    return(dict_FC_S101)


def parse_docx(docx_filepath):
    doc = zipfile.ZipFile(docx_filepath).read('word/document.xml')
    root = ET.fromstring(doc)
    return(root)
    

# Fonction permettant de lire le DCEG  
def read_DCEG_S101(DCEG_filepath):
    dict_DCEG = dict()
    
    root = parse_docx(DCEG_filepath)
    
    # Lecture de toutes les sections du document
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    body = root.find('w:body', ns)  # find the XML "body" tag

    sections = []
    for el in body.iter():
        tag = el.tag.split('}')[-1]
        if tag == 'p':
            sections.append(el)
    
    # Identifie si une section est un "Titre X"
    def is_titreX_section(para, X):
        """Returns True if the given paragraph section has been styled as a HeadingX"""
        return_val = False
        heading_style_elem = para.find(".//w:pStyle[@w:val='Titre"+X+"']", ns)
        if heading_style_elem is not None:
            return_val = True
        return return_val
    
    # Renvoi le texte d'une section donnée
    def get_section_text(s):
        """Returns the joined text of the text elements under the given paragraph tag"""
        return_val = None
        text_elems = s.findall('.//w:t', ns)
        if len(text_elems) != 0:
            return_val = ''.join([t.text for t in text_elems])
        return return_val    
    
    # Structuration des sections dans un dictionaire
    lvl = 0 # Niveau de titre où l'on se trouve dans l'arborescence
    num_titres = np.array([0,0,0,0]) # n° des titres en fonction du niveau
    num_section = np.array([0,0,0,0]) # n° du § des chapitres en fonction du niveau
    
    for s in sections:
        text = get_section_text(s)

        # Identification si une section est un titre
        is_titre = False
        for i in range(1,5):
            if is_titreX_section(s, str(i)) and text != 'CONTENTS':
                is_titre = True
                lvl = i
        
        # Ajout des titres au dictionaire
        if is_titre and text != None:
            num_titres[lvl-1] += 1
            num_titres[lvl:] = 0 # RàZ des n° de titres plus bas
            num_section[lvl-1:] = 0 # RàZ des n° de para de même niveau ou moins
            num_T = '.'.join([str(x) for x in num_titres if x != 0])
            
            if lvl == 1:
                dict_DCEG[num_T] = dict()
                dict_DCEG[num_T]['titre'] = text
                
            elif lvl == 2:
                dict_DCEG['.'.join(num_T.split('.')[:1])][num_T] = dict()
                dict_DCEG['.'.join(num_T.split('.')[:1])][num_T]['titre'] = text

            elif lvl == 3:
                dict_DCEG['.'.join(num_T.split('.')[:1])]['.'.join(num_T.split('.')[:2])][num_T] = dict()
                dict_DCEG['.'.join(num_T.split('.')[:1])]['.'.join(num_T.split('.')[:2])][num_T]['titre'] = text

            elif lvl == 4:
                dict_DCEG['.'.join(num_T.split('.')[:1])]['.'.join(num_T.split('.')[:2])]['.'.join(num_T.split('.')[:3])][num_T] = dict()
                dict_DCEG['.'.join(num_T.split('.')[:1])]['.'.join(num_T.split('.')[:2])]['.'.join(num_T.split('.')[:3])][num_T]['titre'] = text
    
        # Ajout des § au dictionaire
        elif not is_titre and lvl != 0 and text != None:
            num_section[lvl-1] += 1
            num_S = str(num_section[lvl-1])
            section_str = '§'+num_S
            
            if lvl == 1:
                dict_DCEG[num_T][section_str] = text
                
            elif lvl == 2:
                dict_DCEG['.'.join(num_T.split('.')[:1])][num_T][section_str] = text
            
            elif lvl ==3:
                dict_DCEG['.'.join(num_T.split('.')[:1])]['.'.join(num_T.split('.')[:2])][num_T][section_str] = text
                
            elif lvl == 4:
                dict_DCEG['.'.join(num_T.split('.')[:1])]['.'.join(num_T.split('.')[:2])]['.'.join(num_T.split('.')[:3])][num_T][section_str] = text

    return(dict_DCEG)