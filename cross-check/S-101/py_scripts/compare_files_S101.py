# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 14:31:46 2023

@author: hchonavel
"""

from unidecode import unidecode


# Comparaison des SimpleAttributes du FC S-101 au DCEG S-101
def compare_FC_DCEG_S101_SimpleAttributes(dict_FC_S101, dict_DCEG_S101):
    
    ###########################################################################
    # Sens FC vers DCEG
    ###########################################################################
    
    #_____________________________SimpleAttributes_____________________________
    omission_SimpleAttributes_DCEG = list()
    
    omission_SimpleAttributes_definition_DCEG = list()
    inconsistent_SimpleAttributes_definition = list()
    
    omission_SimpleAttributes_alias_DCEG = list()
    inconsistent_SimpleAttributes_alias = list()
 
    inconsistent_SimpleAttributes_type = list()
    
    ommission_SimpleAttributes_enum_DCEG = list()
    ommission_SimpleAttributes_enum_FC = list()
    inconsitent_SimpleAttributes_enum_label = list()
    inconsitent_SimpleAttributes_enum_def = list()
    
    inconsistent_SimpleAttributes_code_FC = list()
    
    # Les attributs simples correspondent aux chapitres 27, 28 et 30 dans le DCEG
    SimpleAttributes_DCEG_dict = {**dict_DCEG_S101['27'],**dict_DCEG_S101['28'],**dict_DCEG_S101['30'],**dict_DCEG_S101['32']}
    
    DCEG_chap_lst = list(SimpleAttributes_DCEG_dict.keys())[1:]
#    SimpleAttribute_DCEG_lst_ = [SimpleAttributes_DCEG_dict[chap]['§1'].split(':')[0] for chap in DCEG_chap_lst]
    SimpleAttribute_DCEG_lst_ = [SimpleAttributes_DCEG_dict[chap]['titre'].split(' (')[0] for chap in DCEG_chap_lst]
    SimpleAttribute_DCEG_lst = [unidecode(x).lower() for x in SimpleAttribute_DCEG_lst_]
    
    for SimpleAttribute_FC in dict_FC_S101['SimpleAttributes'].keys():
        SimpleAttribute_FC_dict = dict_FC_S101['SimpleAttributes'][SimpleAttribute_FC]
        FC_name = SimpleAttribute_FC_dict['name']
        
        if '–' in FC_name.split(' '):
            FC_name = FC_name.replace('–','-')
        
        #__________Présence de l'attribut dans le DCEG__________
        if FC_name.lower() in SimpleAttribute_DCEG_lst:
            ind_DCEG = [i for i in range(len(SimpleAttribute_DCEG_lst)) if
                        SimpleAttribute_DCEG_lst[i]==FC_name.lower()][0]
            chap_DCEG = DCEG_chap_lst[ind_DCEG]
            SimpleAttribute_DCEG_dict = SimpleAttributes_DCEG_dict[chap_DCEG]
            
            #__________Cohérence de la définition__________
            FC_definition = SimpleAttribute_FC_dict['definition']
            for el in [' a. ',' b. ',' c. ',' d. ',' e. ']:
                FC_definition = FC_definition.replace(el,' ')
                
            text_para_bool = False
            if len(SimpleAttribute_DCEG_dict['§1'].split('IHO Definition: '+FC_name.upper().replace('-','–')+'. ')) > 1:
                text_para = SimpleAttribute_DCEG_dict['§1'].split('IHO Definition: '+FC_name.upper().replace('-','–')+'. ')[1]
                text_para_bool = True
            elif len(SimpleAttribute_DCEG_dict['§1'].split('IHO Definition: '+FC_name.upper()+'. ')) > 1:
                text_para = SimpleAttribute_DCEG_dict['§1'].split('IHO Definition: '+FC_name.upper()+'. ')[1]
                text_para_bool = True
                
            if text_para_bool == True:
                # éléments qui ne sont pas pris en compte dans la définition du FC
                if '. (' in text_para:
                    text_para = text_para.split('. (')[0]+'.'
                DCEG_definition = text_para
                num_para = 2
                str_para = '§'+str(num_para)
                while 'Attribute Type:' not in SimpleAttribute_DCEG_dict[str_para] and 'Indication:' not in SimpleAttribute_DCEG_dict[str_para]:
                    DCEG_definition +=  ' '
                    text_para = SimpleAttribute_DCEG_dict[str_para]
                    # éléments qui ne sont pas pris en compte dans la définition du FC
                    if '. (' in text_para:
                        text_para = text_para.split('. (')[0]+'.'
                    DCEG_definition += text_para
                    num_para += 1
                    str_para = '§'+str(num_para)

                DCEG_definition = DCEG_definition.replace('…','...')
                DCEG_definition = DCEG_definition.replace('‘',"'")
                DCEG_definition = DCEG_definition.replace('’',"'")
                DCEG_definition = DCEG_definition.replace('“','"')
                    
                if not FC_definition.lower() == DCEG_definition.lower():
                    inconsistent_SimpleAttributes_definition.append((FC_name,FC_definition,DCEG_definition))
            
            else:
                omission_SimpleAttributes_definition_DCEG.append(FC_name)
        
            #__________Cohérence de l'alias__________
            if 'alias' in SimpleAttribute_FC_dict.keys():
                FC_alias_lst = SimpleAttribute_FC_dict['alias']
                DCEG_titre = SimpleAttribute_DCEG_dict['titre']
                if '(' in DCEG_titre and ')' in DCEG_titre:
                    DCEG_alias_lst = DCEG_titre.split('(')[-1].split(')')[0].split(', ')
                    if not FC_alias_lst == DCEG_alias_lst:
                        inconsistent_SimpleAttributes_alias.append((FC_name,FC_alias_lst,DCEG_alias_lst))
                else:
                    omission_SimpleAttributes_alias_DCEG.append((FC_name,FC_alias_lst))
                    
            #__________Cohérence du type__________
            FC_type = SimpleAttribute_FC_dict['valueType']
            DCEG_type = [x.split('Attribute Type: ')[1] for x in SimpleAttribute_DCEG_dict.values() if 'Attribute Type: ' in x][0]
            
            if FC_type != DCEG_type.lower():
                inconsistent_SimpleAttributes_type.append((FC_name,FC_type,DCEG_type))
            
            #__________Cohérence des items dans le cas d'une énumération__________
            if FC_type == 'enumeration':
                DCEG_enum_label_lst = list()
                DCEG_enum_def_lst = list()
                FC_enum_label_lst = list()
                FC_enum_def_lst = list()
                
                enum_start = [i for i in range(len(SimpleAttribute_DCEG_dict.values())) if 'Attribute Type:' in list(SimpleAttribute_DCEG_dict.values())[i]][0]+1
                enum_end = [i for i in range(len(SimpleAttribute_DCEG_dict.values())) if 'Remarks:' in list(SimpleAttribute_DCEG_dict.values())[i]][0]
                
                first_enum = True
                DCEG_enum_def = str()
                for text_para in list(SimpleAttribute_DCEG_dict.values())[enum_start:enum_end]:
                    if text_para[-1]==' ':
                        text_para = text_para[:-1]
                    if text_para[-1] not in ['.',':']:
                        DCEG_enum_label = text_para
                        DCEG_enum_label_lst.append(DCEG_enum_label)
                        if first_enum:
                            first_enum = False
                        else:
                            DCEG_enum_def_lst.append(DCEG_enum_def)
                        DCEG_enum_def = str()
                    else:
                        if '. (' in text_para:
                            text_para = text_para.split('. (')[0]+'.'
                        if not 'IHO Definition: ' in text_para:
                            if DCEG_enum_def:
                                DCEG_enum_def += ' '+text_para
                            else:
                                DCEG_enum_def = '"IHO Definition: " missing in the DCEG'
                        else:
                            DCEG_enum_def += text_para.split('IHO Definition: ')[1]
                DCEG_enum_def_lst.append(DCEG_enum_def)

                for FC_enum in SimpleAttribute_FC_dict['listedValues'].values():
                    FC_enum_label = FC_enum['label']
                    FC_enum_def = FC_enum['definition']
                    FC_enum_label_lst.append(FC_enum_label)
                    FC_enum_def_lst.append(FC_enum_def)

                if len(FC_enum_label_lst) < len(DCEG_enum_label_lst):
                    missing_enum_FC = [x for x in DCEG_enum_label_lst if x not in [y.lower() for y in FC_enum_label_lst]]
                    ommission_SimpleAttributes_enum_FC = (FC_name,missing_enum_FC)
                    
                elif len(DCEG_enum_label_lst) < len(FC_enum_label_lst):
                    missing_enum_DCEG = [x for x in [y.lower() for y in FC_enum_label_lst] if x not in DCEG_enum_label_lst]
                    ommission_SimpleAttributes_enum_DCEG = (FC_name,missing_enum_DCEG)
                
                if len(FC_enum_label_lst) == len(DCEG_enum_label_lst):
                    for i in range(len(FC_enum_label_lst)):
                        FC_enum_label = FC_enum_label_lst[i].lower()
                        DCEG_enum_label = DCEG_enum_label_lst[i].lower()
                        DCEG_enum_label = DCEG_enum_label.replace('’',"'")
                        if FC_enum_label != DCEG_enum_label:
                            inconsitent_SimpleAttributes_enum_label.append((FC_name,FC_enum_label,DCEG_enum_label))
                       
                    for i in range(len(FC_enum_label_lst)):
                        if FC_enum_def_lst[i] is None:
                            FC_enum_def = ""
                        else:
                            FC_enum_def = FC_enum_def_lst[i].lower()
                        DCEG_enum_def = DCEG_enum_def_lst[i].lower()

#                        if 'seabed' in DCEG_enum_def and 'sea bed' in FC_enum_def:
#                            print(FC_name+' - '+FC_enum_label_lst[i])
                        
#                        if ' also known as' in DCEG_enum_def or ' also called' in DCEG_enum_def:
#                            print(FC_name+' - '+FC_enum_label_lst[i])
                        
#                        if ('feature' in DCEG_enum_def and 'object' in FC_enum_def) or ('features' in DCEG_enum_def and 'objects' in FC_enum_def):
#                            print(FC_name+' - '+FC_enum_label_lst[i])
                        
                        DCEG_enum_def = DCEG_enum_def.replace('…','...')
                        DCEG_enum_def = DCEG_enum_def.replace('‘',"'")
                        DCEG_enum_def = DCEG_enum_def.replace('’',"'")
                        DCEG_enum_def = DCEG_enum_def.replace('“',"'")
                        DCEG_enum_def = DCEG_enum_def.replace('”',"'")
                        DCEG_enum_def = DCEG_enum_def.replace('–','-')
                        DCEG_enum_def = DCEG_enum_def.replace('\xa0',' ')
                        
                        DCEG_enum_def = DCEG_enum_def.split(' also known as')[0]
                        DCEG_enum_def = DCEG_enum_def.split(' also called')[0]

                        if 'seabed' in DCEG_enum_def and 'sea bed' in FC_enum_def:
                            DCEG_enum_def= DCEG_enum_def.replace('seabed','sea bed')
                            
                        if 'feature' in DCEG_enum_def and 'object' in FC_enum_def:
                            DCEG_enum_def = DCEG_enum_def.replace('feature','object')

                        if 'features' in DCEG_enum_def and 'objects' in FC_enum_def:
                            DCEG_enum_def = DCEG_enum_def.replace('features','objects')
                            
                        if FC_enum_def != DCEG_enum_def:
                            FC_enum_label = FC_enum_label_lst[i]
                            inconsitent_SimpleAttributes_enum_def.append((FC_name,FC_enum_label,FC_enum_def,DCEG_enum_def))

        else:
            omission_SimpleAttributes_DCEG.append(FC_name)
            """
            Il s'agit en général d'une erreur dans l'écriture du titre du chapitre dans le DCEG
            """
        
        #__________Vérification construction du FCcode__________
        FC_code = SimpleAttribute_FC_dict['code']
        if not FC_name[0].lower()+''.join(FC_name.split(' '))[1:]:
            inconsistent_SimpleAttributes_code_FC.append((FC_name,FC_code))

    
    return(omission_SimpleAttributes_DCEG,
           omission_SimpleAttributes_definition_DCEG,
           inconsistent_SimpleAttributes_definition,
           omission_SimpleAttributes_alias_DCEG,
           inconsistent_SimpleAttributes_alias,
           inconsistent_SimpleAttributes_type,
           ommission_SimpleAttributes_enum_DCEG,
           ommission_SimpleAttributes_enum_FC,
           inconsitent_SimpleAttributes_enum_label,
           inconsitent_SimpleAttributes_enum_def,
           inconsistent_SimpleAttributes_code_FC)


# Comparaison des ComplexAttributes du FC S-101 au DCEG S-101
def compare_FC_DCEG_S101_ComplexAttributes(dict_FC_S101, dict_DCEG_S101):
    
    dict_SimpleAttributes_code2name = dict(zip([dict_FC_S101['SimpleAttributes'][attr]['code'] for attr in dict_FC_S101['SimpleAttributes']], dict_FC_S101['SimpleAttributes'].keys()))
    dict_ComplexAttributes_code2name = dict(zip([dict_FC_S101['ComplexAttributes'][attr]['code'] for attr in dict_FC_S101['ComplexAttributes']], dict_FC_S101['ComplexAttributes'].keys()))
    dict_Attributes_code2name = {**dict_SimpleAttributes_code2name, **dict_ComplexAttributes_code2name}
    
    ###########################################################################
    # Sens FC vers DCEG
    ###########################################################################
    
    #_____________________________ComplexAttributes____________________________
    omission_ComplexAttributes_DCEG = list()
    
    inconsistent_ComplexAttributes_DCEG_title = list()
    
    inconsistent_ComplexAttributes_definition = list()
    omission_ComplexAttributes_definition_DCEG = list()
    
    inconsistent_ComplexAttributes_alias = list()
    omission_ComplexAttributes_alias_DCEG = list()

    inconsistent_ComplexAttributes_subAttributes = list()
    
    # Les attributs complexes correspondent au chapitre 29 dans le DCEG
    ComplexAttributes_DCEG_dict = dict_DCEG_S101['29']

    DCEG_chap_lst = list(ComplexAttributes_DCEG_dict.keys())[1:]
    ComplexAttributes_DCEG_lst_ = [ComplexAttributes_DCEG_dict[chap]['titre'].split(' (')[0] for chap in DCEG_chap_lst]
    ComplexAttributes_DCEG_lst = [unidecode(x).lower() for x in ComplexAttributes_DCEG_lst_]
    
    for ComplexAttribute_FC in dict_FC_S101['ComplexAttributes'].keys():
        ComplexAttribute_FC_dict = dict_FC_S101['ComplexAttributes'][ComplexAttribute_FC]
        FC_name = ComplexAttribute_FC_dict['name']
        
        #__________Présence de l'attribut dans le DCEG__________
        if FC_name.lower() in ComplexAttributes_DCEG_lst:
            ind_DCEG = [i for i in range(len(ComplexAttributes_DCEG_lst)) if
                        ComplexAttributes_DCEG_lst[i]==FC_name.lower()][0]
            chap_DCEG = DCEG_chap_lst[ind_DCEG]
            ComplexAttribute_DCEG_dict = ComplexAttributes_DCEG_dict[chap_DCEG]

            #__________Cohérence titre / sous-titre DCEG__________
            title_DCEG = ComplexAttribute_DCEG_dict['titre']
            subtitle_DCEG = ComplexAttribute_DCEG_dict['§1'].split('IHO Definition: ')[1].split('.')[0]
            if not title_DCEG.split(' (')[0] == subtitle_DCEG.lower():
                inconsistent_ComplexAttributes_DCEG_title.append((title_DCEG,subtitle_DCEG))
            
            #__________Cohérence de la définition__________
            FC_definition = ComplexAttribute_FC_dict['definition']
            for el in [' a. ',' b. ',' c. ',' d. ',' e. ']:
                FC_definition = FC_definition.replace(el,' ')

            if len(ComplexAttribute_DCEG_dict['§1'].split('IHO Definition: '+subtitle_DCEG+'. ')) > 1:
                text_para = ComplexAttribute_DCEG_dict['§1'].split('IHO Definition: '+subtitle_DCEG+'. ')[1]
                # éléments qui ne sont pas pris en compte dans la définition du FC
                if '. (' in text_para:
                    text_para = text_para.split('. (')[0]+'.'
                DCEG_definition = text_para
                num_para = 2
                str_para = '§'+str(num_para)
                while 'Attribute Type:' not in ComplexAttribute_DCEG_dict[str_para] and 'Indication:' not in ComplexAttribute_DCEG_dict[str_para]:
                    DCEG_definition +=  ' '
                    text_para = ComplexAttribute_DCEG_dict[str_para]
                    # éléments qui ne sont pas pris en compte dans la définition du FC
                    if '. (' in text_para:
                        text_para = text_para.split('. (')[0]+'.'
                    DCEG_definition += text_para
                    num_para += 1
                    str_para = '§'+str(num_para)

                DCEG_definition = DCEG_definition.replace('…','...')
                DCEG_definition = DCEG_definition.replace('‘',"'")
                DCEG_definition = DCEG_definition.replace('’',"'")
                
                if len(DCEG_definition)!=0:
                    if DCEG_definition[-1]==' ':
                        DCEG_definition = DCEG_definition[:-1]
                    
                if not FC_definition.lower() == DCEG_definition.lower():
                    inconsistent_ComplexAttributes_definition.append((FC_name,FC_definition,DCEG_definition))
            
            else:
                omission_ComplexAttributes_definition_DCEG.append(FC_name)

            #__________Cohérence de l'alias__________
            if 'alias' in ComplexAttribute_FC_dict.keys():
                FC_alias_lst = ComplexAttribute_FC_dict['alias']
                DCEG_titre = ComplexAttribute_DCEG_dict['titre']
                if '(' in DCEG_titre and ')' in DCEG_titre:
                    DCEG_alias_lst = DCEG_titre.split('(')[-1].split(')')[0].split(', ')
                    if not FC_alias_lst == DCEG_alias_lst:
                        inconsistent_ComplexAttributes_alias.append((FC_name,FC_alias_lst,DCEG_alias_lst))
                else:
                    omission_ComplexAttributes_alias_DCEG.append((FC_name,FC_alias_lst))

            #__________Cohérence des sous attributs__________
            FC_subAttributes_lst = [dict_Attributes_code2name[x].lower() for x in list(ComplexAttribute_FC_dict['subAttributes'].keys())]
            
            DCEG_subAttributes_lst = list()
            
            subAtt_bool = False
            for value in ComplexAttribute_DCEG_dict.values():
                if 'Sub-attributes:' in value:
                    subAtt_bool = True
                    value = value.split('Sub-attributes:')[1].lstrip()
                if 'Remarks:' in value:
                    subAtt_bool = False
                if subAtt_bool:
                    subAttribute = value.split('see clause')[0].rstrip()
                    DCEG_subAttributes_lst.append(subAttribute)
            
            if not FC_subAttributes_lst == DCEG_subAttributes_lst:
                inconsistent_ComplexAttributes_subAttributes.append((FC_name,list(ComplexAttribute_FC_dict['subAttributes'].keys()),[dict_Attributes_code2name[x] for x in list(ComplexAttribute_FC_dict['subAttributes'].keys())],DCEG_subAttributes_lst))
            
        else:
            omission_ComplexAttributes_DCEG.append(FC_name)
   
    return(omission_ComplexAttributes_DCEG,
           inconsistent_ComplexAttributes_DCEG_title,
           inconsistent_ComplexAttributes_definition,
           omission_ComplexAttributes_definition_DCEG,
           inconsistent_ComplexAttributes_alias,
           omission_ComplexAttributes_alias_DCEG,
           inconsistent_ComplexAttributes_subAttributes)

    
# Comparaison des Roles du FC S-101 au DCEG S-101
def compare_FC_DCEG_S101_Roles(dict_FC_S101, dict_DCEG_S101):

    ###########################################################################
    # Sens FC vers DCEG
    ###########################################################################
    
    #__________________________________Roles___________________________________
    omission_Roles_DCEG = list()
    
    inconsistent_Roles_DCEG_title = list()
    
    inconsistent_Roles_definition = list()
    omission_Roles_definition_DCEG = list()

    # Les roles correspondent au chapitre 26 dans le DCEG
    Roles_DCEG_dict = dict_DCEG_S101['26']

    DCEG_chap_lst = list(Roles_DCEG_dict.keys())[1:]
    Roles_DCEG_lst_ = [Roles_DCEG_dict[chap]['titre'].split(' (')[0] for chap in DCEG_chap_lst]
    Roles_DCEG_lst = [unidecode(x).lower() for x in Roles_DCEG_lst_]    
    
    for Role_FC in dict_FC_S101['Roles'].keys():
        Role_FC_dict = dict_FC_S101['Roles'][Role_FC]
        FC_name = Role_FC_dict['name']
        
        #__________Présence du role dans le DCEG__________
        if FC_name.lower() in Roles_DCEG_lst:
            ind_DCEG = [i for i in range(len(Roles_DCEG_lst)) if
                        Roles_DCEG_lst[i]==FC_name.lower()][0]
            chap_DCEG = DCEG_chap_lst[ind_DCEG]
            Role_DCEG_dict = Roles_DCEG_dict[chap_DCEG]

            #__________Cohérence titre / sous-titre DCEG__________
            title_DCEG = Role_DCEG_dict['titre']
            subtitle_DCEG = Role_DCEG_dict['§1'].split('IHO Definition: ')[1].split('.')[0]
            if not title_DCEG.lower() == subtitle_DCEG.lower():
                inconsistent_Roles_DCEG_title.append((title_DCEG,subtitle_DCEG))
            
            #__________Cohérence de la définition__________
            FC_definition = Role_FC_dict['definition']
            for el in [' a. ',' b. ',' c. ',' d. ',' e. ']:
                FC_definition = FC_definition.replace(el,' ')

            if len(Role_DCEG_dict['§1'].split('IHO Definition: '+subtitle_DCEG+'. ')) > 1:
                text_para = Role_DCEG_dict['§1'].split('IHO Definition: '+subtitle_DCEG+'. ')[1]
                # éléments qui ne sont pas pris en compte dans la définition du FC
                if '. (' in text_para:
                    text_para = text_para.split('. (')[0]+'.'
                DCEG_definition = text_para

                DCEG_definition = DCEG_definition.replace('…','...')
                DCEG_definition = DCEG_definition.replace('‘',"'")
                DCEG_definition = DCEG_definition.replace('’',"'")
                
                if len(DCEG_definition)!=0:
                    if DCEG_definition[-1]==' ':
                        DCEG_definition = DCEG_definition[:-1]
                    
                if not FC_definition.lower() == DCEG_definition.lower():
                    inconsistent_Roles_definition.append((FC_name,FC_definition,DCEG_definition))
            
            else:
                omission_Roles_definition_DCEG.append(FC_name)    
    
        else:
            omission_Roles_DCEG.append(FC_name)    

    return(omission_Roles_DCEG,
           inconsistent_Roles_DCEG_title,
           inconsistent_Roles_definition,
           omission_Roles_definition_DCEG)    

# Comparaison des FeatureAssociations du FC S-101 au DCEG S-101
def compare_FC_DCEG_S101_FeatureAssociations(dict_FC_S101, dict_DCEG_S101):

    dict_roles_code2name = dict(zip([dict_FC_S101['Roles'][role]['code'] for role in dict_FC_S101['Roles']], dict_FC_S101['Roles'].keys()))
    
    ###########################################################################
    # Sens FC vers DCEG
    ###########################################################################
    
    #__________________________________FeatureAssociations___________________________________
    omission_FeatureAssociations_DCEG = list()
    
    inconsistent_FeatureAssociations_DCEG_title = list()
    
    inconsistent_FeatureAssociations_definition = list()
    omission_FeatureAssociations_definition_DCEG = list()
    
    inconsistent_FeatureAssociations_roles =  list()

    # Les FeatureAssociations correspondent au chapitre 25 dans le DCEG
    FeatureAssociations_DCEG_dict = dict_DCEG_S101['25']

    DCEG_chap_lst = [x for x in list(FeatureAssociations_DCEG_dict.keys())[1:] if x[0]!='§'] 
    FeatureAssociations_DCEG_lst_ = [FeatureAssociations_DCEG_dict[chap]['titre'] for chap in DCEG_chap_lst]
    FeatureAssociations_DCEG_lst = [unidecode(x).lower() for x in FeatureAssociations_DCEG_lst_]    
    
    for FeatureAssociation_FC in dict_FC_S101['FeatureAssociations'].keys():
        FeatureAssociation_FC_dict = dict_FC_S101['FeatureAssociations'][FeatureAssociation_FC]
        FC_name = FeatureAssociation_FC_dict['name']
        
        #__________Présence de la feature association dans le DCEG__________
        if FC_name.lower() in FeatureAssociations_DCEG_lst:
            ind_DCEG = [i for i in range(len(FeatureAssociations_DCEG_lst)) if
                        FeatureAssociations_DCEG_lst[i]==FC_name.lower()][0]
            chap_DCEG = DCEG_chap_lst[ind_DCEG]
            FeatureAssociation_DCEG_dict = FeatureAssociations_DCEG_dict[chap_DCEG]

            #__________Cohérence titre / sous-titre DCEG__________
            title_DCEG = FeatureAssociation_DCEG_dict['titre']
            subtitle_DCEG = FeatureAssociation_DCEG_dict['§1'].split('IHO Definition: ')[1].split('.')[0]
            if not title_DCEG.lower() == subtitle_DCEG.lower():
                inconsistent_FeatureAssociations_DCEG_title.append((title_DCEG,subtitle_DCEG))
            
            #__________Cohérence de la définition__________
            FC_definition = FeatureAssociation_FC_dict['definition']
            for el in [' a. ',' b. ',' c. ',' d. ',' e. ']:
                FC_definition = FC_definition.replace(el,' ')

            if len(FeatureAssociation_DCEG_dict['§1'].split('IHO Definition: '+subtitle_DCEG+'. ')) > 1:
                text_para = FeatureAssociation_DCEG_dict['§1'].split('IHO Definition: '+subtitle_DCEG+'. ')[1]
                # éléments qui ne sont pas pris en compte dans la définition du FC
                if '. (' in text_para:
                    text_para = text_para.split('. (')[0]+'.'
                DCEG_definition = text_para

                DCEG_definition = DCEG_definition.replace('…','...')
                DCEG_definition = DCEG_definition.replace('‘',"'")
                DCEG_definition = DCEG_definition.replace('’',"'")
                
                if len(DCEG_definition)!=0:
                    if DCEG_definition[-1]==' ':
                        DCEG_definition = DCEG_definition[:-1]
                    
                if not FC_definition.lower() == DCEG_definition.lower():
                    inconsistent_FeatureAssociations_definition.append((FC_name,FC_definition,DCEG_definition))
            
            else:
                omission_FeatureAssociations_definition_DCEG.append(FC_name)    

            #__________Cohérence des rôles__________
            FC_Roles_lst = [dict_roles_code2name[x].lower() for x in FeatureAssociation_FC_dict['roles']]
            
            DCEG_Roles_lst = list()
            for i in range(len(FeatureAssociation_DCEG_dict.values())):
                key = list(FeatureAssociation_DCEG_dict.keys())[i]
                value = FeatureAssociation_DCEG_dict[key]
                
                if value == 'Role':
                    key_1 = list(FeatureAssociation_DCEG_dict.keys())[i+4]
                    role_1 = FeatureAssociation_DCEG_dict[key_1]
                    DCEG_Roles_lst.append(role_1.lower())
                    key_2 = list(FeatureAssociation_DCEG_dict.keys())[i+8]
                    role_2 = FeatureAssociation_DCEG_dict[key_2]
                    DCEG_Roles_lst.append(role_2.lower()) 
            
            if not FC_Roles_lst == DCEG_Roles_lst:
                inconsistent_FeatureAssociations_roles.append((FC_name,FC_Roles_lst,DCEG_Roles_lst))
            
        else:
            omission_FeatureAssociations_DCEG.append(FC_name)    

    return(omission_FeatureAssociations_DCEG,
           inconsistent_FeatureAssociations_DCEG_title,
           inconsistent_FeatureAssociations_definition,
           omission_FeatureAssociations_definition_DCEG,
           inconsistent_FeatureAssociations_roles)

# Comparaison des InformationTypes du FC S-101 au DCEG S-101
def compare_FC_DCEG_S101_InformationTypes(dict_FC_S101, dict_DCEG_S101):
    
    dict_SimpleAttributes_code2name = dict(zip([dict_FC_S101['SimpleAttributes'][attr]['code'] for attr in dict_FC_S101['SimpleAttributes']], dict_FC_S101['SimpleAttributes'].keys()))
    dict_ComplexAttributes_code2name = dict(zip([dict_FC_S101['ComplexAttributes'][attr]['code'] for attr in dict_FC_S101['ComplexAttributes']], dict_FC_S101['ComplexAttributes'].keys()))
    dict_Attributes_code2name = {**dict_SimpleAttributes_code2name, **dict_ComplexAttributes_code2name}
    
    ###########################################################################
    # Sens FC vers DCEG
    ###########################################################################
    
    #_____________________________InformationTypes_____________________________
    omission_InformationTypes_DCEG = list()
    
    inconsistent_InformationTypes_DCEG_title = list()
    
    inconsistent_InformationTypes_definition = list()
    omission_InformationTypes_definition_DCEG = list()
    
    inconsistent_InformationTypes_attributes = list()
    inconsistent_InformationTypes_multiplicity = list()
    
    # Les Information Types correspondent au chapitre 24 dans le DCEG
    InformationTypes_DCEG_dict = dict_DCEG_S101['24']
    
    DCEG_chap_lst = [x for x in list(InformationTypes_DCEG_dict.keys())[1:] if x[0]!='§'] 
    InformationTypes_DCEG_lst_ = [InformationTypes_DCEG_dict[chap]['titre'] for chap in DCEG_chap_lst]
    InformationTypes_DCEG_lst = [unidecode(x).lower() for x in InformationTypes_DCEG_lst_]    
    
    for InformationType_FC in dict_FC_S101['InformationTypes'].keys():
        InformationType_FC_dict = dict_FC_S101['InformationTypes'][InformationType_FC]
        FC_name = InformationType_FC_dict['name']
        
        #__________Présence de l'information type dans le DCEG__________
        if FC_name.lower() in InformationTypes_DCEG_lst:
            ind_DCEG = [i for i in range(len(InformationTypes_DCEG_lst)) if
                        InformationTypes_DCEG_lst[i]==FC_name.lower()][0]
            chap_DCEG = DCEG_chap_lst[ind_DCEG]
            InformationType_DCEG_dict = InformationTypes_DCEG_dict[chap_DCEG]

            #__________Cohérence titre / sous-titre DCEG__________
            title_DCEG = InformationType_DCEG_dict['titre']
            subtitle_DCEG_1 = InformationType_DCEG_dict['§1'].split('IHO Definition: ')[1].split('.')[0]
            subtitle_DCEG_2 = InformationType_DCEG_dict['§2'].split('S-101 Information Type: ')[1]
            if not title_DCEG.lower() == subtitle_DCEG_1.lower() or not title_DCEG.lower() == subtitle_DCEG_2.lower():
                inconsistent_InformationTypes_DCEG_title.append((title_DCEG,subtitle_DCEG_1,subtitle_DCEG_2)) 
    
            #__________Cohérence de la définition__________
            FC_definition = InformationType_FC_dict['definition']
            for el in [' a. ',' b. ',' c. ',' d. ',' e. ']:
                FC_definition = FC_definition.replace(el,' ')

            if len(InformationType_DCEG_dict['§1'].split('IHO Definition: ')[1].split('. ')) > 1:
                text_para = '. '.join(InformationType_DCEG_dict['§1'].split('IHO Definition: ')[1].split('. ')[1:])
                # éléments qui ne sont pas pris en compte dans la définition du FC
                if '. (' in text_para:
                    text_para = text_para.split('. (')[0]+'.'
                DCEG_definition = text_para

                DCEG_definition = DCEG_definition.replace('…','...')
                DCEG_definition = DCEG_definition.replace('‘',"'")
                DCEG_definition = DCEG_definition.replace('’',"'")
                
                if len(DCEG_definition)!=0:
                    if DCEG_definition[-1]==' ':
                        DCEG_definition = DCEG_definition[:-1]
                    
                if not FC_definition.lower() == DCEG_definition.lower():
                    inconsistent_InformationTypes_definition.append((FC_name,FC_definition,DCEG_definition))
            
            else:
                omission_InformationTypes_definition_DCEG.append(FC_name)

            #__________Cohérence des attributs__________
            FC_Attributes_lst = [dict_Attributes_code2name[x].lower() for x in InformationType_FC_dict['attributes']]
            FC_Multiplicity_lst = [x['multiplicity'] for x in InformationType_FC_dict['attributes'].values()]
            
            DCEG_Attributes_lst = list()
            DCEG_Multiplicity_lst = list()
            
            # Récupérer directement l'ind qui va bien pour le 'S-101 Attribute'
            ind = list(InformationType_DCEG_dict.values()).index('S-101 Attribute')
            
            ind_att = ind+5
            key_att = list(InformationType_DCEG_dict.keys())[ind_att]
            attribute = InformationType_DCEG_dict[key_att]
                    
            ind_= ind_att + 1
            key_ = list(InformationType_DCEG_dict.keys())[ind_]
            value_ = InformationType_DCEG_dict[key_]
            while not (value_[0] in ['0','1','*'] and value_[1]==',' and value_[2] in ['0','1','*']):
                ind_= ind_ + 1
                key_ = list(InformationType_DCEG_dict.keys())[ind_]
                value_ = InformationType_DCEG_dict[key_]
            ind_mul = ind_
            multiplicity = value_[:3]

            if attribute[0]!= ' ':
                DCEG_Attributes_lst.append(attribute)
                DCEG_Multiplicity_lst.append(multiplicity)
            
            while InformationType_DCEG_dict[list(InformationType_DCEG_dict.keys())[ind_mul+1]] != 'Feature Associations':
                
                ind_att = ind_mul+1
                key_att = list(InformationType_DCEG_dict.keys())[ind_att]
                attribute = InformationType_DCEG_dict[key_att]
                        
                ind_= ind_att + 1
                key_ = list(InformationType_DCEG_dict.keys())[ind_]
                value_ = InformationType_DCEG_dict[key_]
                
                while not (value_[0] in ['0','1','*'] and value_[1]==',' and value_[2] in ['0','1','*']):
                    ind_= ind_ + 1
                    key_ = list(InformationType_DCEG_dict.keys())[ind_]
                    value_ = InformationType_DCEG_dict[key_]
                ind_mul = ind_
                multiplicity = value_[:3]
                
                
                
                if attribute[0]!= ' ':
                    DCEG_Attributes_lst.append(attribute)
                    DCEG_Multiplicity_lst.append(multiplicity)
            
            if not FC_Attributes_lst == [x.lower() for x in DCEG_Attributes_lst]:
                inconsistent_InformationTypes_attributes.append((FC_name,FC_Attributes_lst,DCEG_Attributes_lst))
            
            if not FC_Multiplicity_lst == DCEG_Multiplicity_lst:
                inconsistent_InformationTypes_multiplicity.append((FC_name,FC_Attributes_lst,FC_Multiplicity_lst,DCEG_Multiplicity_lst))
                
        else:
            omission_InformationTypes_DCEG.append(FC_name) 
    
    return(omission_InformationTypes_DCEG,
           inconsistent_InformationTypes_DCEG_title,
           inconsistent_InformationTypes_definition,
           omission_InformationTypes_definition_DCEG,
           inconsistent_InformationTypes_attributes,
           inconsistent_InformationTypes_multiplicity)


# Comparaison des FeatureTypes du FC S-101 au DCEG S-101
def compare_FC_DCEG_S101_FeatureTypes(dict_FC_S101, dict_DCEG_S101):
    
    dict_SimpleAttributes_code2name = dict(zip([dict_FC_S101['SimpleAttributes'][attr]['code'] for attr in dict_FC_S101['SimpleAttributes']], dict_FC_S101['SimpleAttributes'].keys()))
    dict_ComplexAttributes_code2name = dict(zip([dict_FC_S101['ComplexAttributes'][attr]['code'] for attr in dict_FC_S101['ComplexAttributes']], dict_FC_S101['ComplexAttributes'].keys()))
    dict_Attributes_code2name = {**dict_SimpleAttributes_code2name, **dict_ComplexAttributes_code2name}
    
    ###########################################################################
    # Sens FC vers DCEG
    ###########################################################################
    
    #_______________________________FeatureTypes_______________________________
    omission_FeatureTypes_DCEG = list()
    
    inconsistent_FeatureTypes_DCEG_title = list()
    
    inconsistent_FeatureTypes_definition = list()
    omission_FeatureTypes_definition_DCEG = list()
    
    inconsistent_FeatureTypes_alias = list()
    omission_FeatureTypes_alias_DCEG = list()
    
    inconsistent_FeatureTypes_attributes = list()
    inconsistent_FeatureTypes_multiplicity = list()
    
    FeatureTypes_multiplicity_error = list()
    
    inconsistent_FeatureTypes_permittedValues = list()
    
    # Les Feature Types correspondent aux chapitres 3 à 23, dans le DCEG
    FeatureTypes_DCEG_dict = {**dict_DCEG_S101['3'], **dict_DCEG_S101['4'],
                              **dict_DCEG_S101['5'], **dict_DCEG_S101['6'],
                              **dict_DCEG_S101['7'], **dict_DCEG_S101['8'],
                              **dict_DCEG_S101['9'], **dict_DCEG_S101['10'],
                              **dict_DCEG_S101['11'], **dict_DCEG_S101['12'],
                              **dict_DCEG_S101['13'], **dict_DCEG_S101['14'],
                              **dict_DCEG_S101['15'], **dict_DCEG_S101['16'],
                              **dict_DCEG_S101['17'], **dict_DCEG_S101['18'],
                              **dict_DCEG_S101['19'], **dict_DCEG_S101['20'],
                              **dict_DCEG_S101['21'], **dict_DCEG_S101['22'],
                              **dict_DCEG_S101['23'], **dict_DCEG_S101['32']}
    
    DCEG_chap_lst = [x for x in list(FeatureTypes_DCEG_dict.keys())[1:] if x[0]!='§']
    FeatureTypes_DCEG_lst_ = [FeatureTypes_DCEG_dict[chap]['titre'] for chap in DCEG_chap_lst]
    FeatureTypes_DCEG_lst = [unidecode(x).lower() for x in FeatureTypes_DCEG_lst_]    
    
    S101_Feature_DCEG_dict = dict()
    for chap_DCEG in DCEG_chap_lst:
        FeatureType_DCEG_dict = FeatureTypes_DCEG_dict[chap_DCEG]
        title_DCEG = FeatureType_DCEG_dict['titre']
        if title_DCEG != "drawing instruction": # Permet de ne pas considérer "drawing instruction" qui est en fait un attribut"
            if '§1' in FeatureType_DCEG_dict.keys():
                if 'IHO Definition:' in FeatureType_DCEG_dict['§1']:
                    i = 2
                    para_num = '§'+str(i)
                    while FeatureType_DCEG_dict[para_num][:5] != 'S-101':
                        i+=1
                        para_num = '§'+str(i)
                    S101_Feature_DCEG = FeatureType_DCEG_dict[para_num].split(': ')[1].split(' (')[0]
                    if S101_Feature_DCEG[0] == ' ':
                        S101_Feature_DCEG = S101_Feature_DCEG[1:]
                    S101_Feature_DCEG_dict[S101_Feature_DCEG.replace('–','-')] = title_DCEG.lower()
    
    for FeatureType_FC in dict_FC_S101['FeatureTypes'].keys():
        FeatureType_FC_dict = dict_FC_S101['FeatureTypes'][FeatureType_FC]
        FC_name = FeatureType_FC_dict['name'].split(' (')[0]
        
        #__________Présence du feature type dans le DCEG__________
        if FC_name in S101_Feature_DCEG_dict.keys():
            title_DCEG = S101_Feature_DCEG_dict[FC_name]
            ind_DCEG = [i for i in range(len(FeatureTypes_DCEG_lst))
            if FeatureTypes_DCEG_lst[i]==title_DCEG.replace('–','-')][0]
            chap_DCEG = DCEG_chap_lst[ind_DCEG]
            FeatureType_DCEG_dict = FeatureTypes_DCEG_dict[chap_DCEG]

            #__________Cohérence de la définition__________
            FC_definition = FeatureType_FC_dict['definition']
            for el in [' a. ',' b. ',' c. ',' d. ',' e. ']:
                FC_definition = FC_definition.replace(el,' ')

            if len(FeatureType_DCEG_dict['§1'].split('IHO Definition: ')[1].split('. ')[1]) > 1:
                text_para = '. '.join(FeatureType_DCEG_dict['§1'].split('IHO Definition: ')[1].split('. ')[1:])
                # éléments qui ne sont pas pris en compte dans la définition du FC
                if '. (' in text_para:
                    text_para = text_para.split('. (')[0]+'.'
                if '.  (' in text_para:
                    text_para = text_para.split('.  (')[0]+'.'
                DCEG_definition = text_para
                num_para = 2
                str_para = '§'+str(num_para)
                while 'Attribute Type:' not in FeatureType_DCEG_dict[str_para] and FeatureType_DCEG_dict[str_para][:5]!='S-101':
                    DCEG_definition +=  ' '
                    text_para = FeatureType_DCEG_dict[str_para]
                    # éléments qui ne sont pas pris en compte dans la définition du FC
                    if '. (' in text_para:
                        text_para = text_para.split('. (')[0]+'.'
                    DCEG_definition += text_para
                    num_para += 1
                    str_para = '§'+str(num_para)

                DCEG_definition = DCEG_definition.replace('…','...')
                DCEG_definition = DCEG_definition.replace('‘',"'")
                DCEG_definition = DCEG_definition.replace('’',"'")
                DCEG_definition = DCEG_definition.replace('“',"'")
                DCEG_definition = DCEG_definition.replace('”',"'")
                
                DCEG_definition = DCEG_definition.replace('A buoy is a floating object moored to the bottom in a particular place, as an aid to navigation or for other specific purposes. ','')
                DCEG_definition = DCEG_definition.replace('A beacon is a prominent specially constructed object forming a conspicuous mark as a fixed aid to navigation or for use in hydrographic survey. ','')
                DCEG_definition = DCEG_definition.replace('A beacon is a prominent, specially constructed object forming a conspicuous mark as a fixed aid to navigation or for use in hydrographic survey. ','')
                
                if not FC_definition.lower() == DCEG_definition.lower():
                    inconsistent_FeatureTypes_definition.append((FC_name,FC_definition,DCEG_definition))
            
            else:
                omission_FeatureTypes_definition_DCEG.append(FC_name)

            #__________Cohérence de l'alias__________
            if 'alias' in FeatureType_FC_dict.keys():
                FC_alias_lst = FeatureType_FC_dict['alias']
                
                # alias
                i = 2
                para_num = '§'+str(i)
                while FeatureType_DCEG_dict[para_num][:5] != 'S-101':
                    i+=1
                    para_num = '§'+str(i)
                    
                if '(' in FeatureType_DCEG_dict[para_num] and ')' in FeatureType_DCEG_dict[para_num]:
                    DCEG_alias_lst_ = FeatureType_DCEG_dict[para_num].split('(')
                    DCEG_alias_lst = [x.split(')')[0] for x in DCEG_alias_lst_[1:]]
                    if not FC_alias_lst == DCEG_alias_lst:
                        inconsistent_FeatureTypes_alias.append((FC_name,FC_alias_lst,DCEG_alias_lst))
                else:
                    omission_FeatureTypes_alias_DCEG.append((FC_name,FC_alias_lst))

            #__________Cohérence des attributs__________
            FC_Attributes_lst = [dict_Attributes_code2name[x].lower() for x in FeatureType_FC_dict['attributes']]
            FC_Multiplicity_lst = [x['multiplicity'] for x in FeatureType_FC_dict['attributes'].values()]
            FC_permittedValues_lst = [x['permittedValues'] for x in FeatureType_FC_dict['attributes'].values() if 'permittedValues' in x.keys()]
            FC_Enumerates_lst = [x for x in FeatureType_FC_dict['attributes'].keys() if 'permittedValues' in FeatureType_FC_dict['attributes'][x].keys()]
            
            DCEG_Attributes_lst = list()
            DCEG_Multiplicity_lst = list()
            DCEG_permittedValues_lst = list()
            
            # Récupérer directement l'ind qui va bien pour le 'S-101 Attribute'
            ind = list(FeatureType_DCEG_dict.values()).index('S-101 Attribute')
            
            ind_att = ind+5
            key_att = list(FeatureType_DCEG_dict.keys())[ind_att]
            attribute = FeatureType_DCEG_dict[key_att]
            DCEG_permittedValues_sublst = list()
            
            ind_= ind_att + 1
            key_ = list(FeatureType_DCEG_dict.keys())[ind_]
            value_ = FeatureType_DCEG_dict[key_]

            while not (len(value_)<=20 and value_[0] in ['0','1','*'] and (value_[1]==',' or value_[1]=='.') and value_[2] in ['0','1','2','*','.']):
                
                if ':' in value_:
                    DCEG_permittedValues_sublst.append(value_.split(':')[0].strip())
                
                ind_= ind_ + 1
                key_ = list(FeatureType_DCEG_dict.keys())[ind_]
                value_ = FeatureType_DCEG_dict[key_]
            
            if len(DCEG_permittedValues_sublst) != 0:
                if attribute[0]!= ' ':
                    DCEG_permittedValues_lst.append(DCEG_permittedValues_sublst)
                DCEG_permittedValues_sublst = list()
            
            ind_mul = ind_
            multiplicity = value_[:3]

            if multiplicity[1]=='.':
                FeatureTypes_multiplicity_error.append((FC_name,attribute,value_))
                    
            if attribute[0]!= ' ': 
                attribute = attribute.replace('–','-')
                attribute = attribute.strip() 
                DCEG_Attributes_lst.append(attribute)
                DCEG_Multiplicity_lst.append(multiplicity)

            while FeatureType_DCEG_dict[list(FeatureType_DCEG_dict.keys())[ind_mul+1]] != 'Feature Associations':
                
                ind_att = ind_mul+1
                key_att = list(FeatureType_DCEG_dict.keys())[ind_att]
                attribute = FeatureType_DCEG_dict[key_att]
                        
                ind_= ind_att + 1
                key_ = list(FeatureType_DCEG_dict.keys())[ind_]
                value_ = FeatureType_DCEG_dict[key_]
                
                while not (len(value_)<=20 and value_[0] in ['0','1','*'] and (value_[1]==',' or value_[1]=='.') and value_[2] in ['0','1','2','*','.']):

                    if ':' in value_:
                        DCEG_permittedValues_sublst.append(value_.split(':')[0].strip())
                    
                    ind_= ind_ + 1
                    key_ = list(FeatureType_DCEG_dict.keys())[ind_]
                    value_ = FeatureType_DCEG_dict[key_]
                    
                ind_mul = ind_
                multiplicity = value_[:3]

                if len(DCEG_permittedValues_sublst) != 0:
                    if attribute[0]!= ' ':
                        DCEG_permittedValues_lst.append(DCEG_permittedValues_sublst)
                    DCEG_permittedValues_sublst = list()
                            
                if multiplicity[1]=='.':
                    FeatureTypes_multiplicity_error.append((FC_name,attribute,value_))                
                
                if attribute[0]!= ' ':
                    attribute = attribute.replace('–','-')
                    attribute = attribute.strip() 
                    DCEG_Attributes_lst.append(attribute)
                    DCEG_Multiplicity_lst.append(multiplicity)
            
            diff_Attributes = list(set(FC_Attributes_lst) - set([x.lower() for x in DCEG_Attributes_lst]))
            if len(diff_Attributes) != 0:
                inconsistent_FeatureTypes_attributes.append((FC_name,diff_Attributes,FC_Attributes_lst,DCEG_Attributes_lst))
            
            if not FC_Multiplicity_lst == DCEG_Multiplicity_lst and len(diff_Attributes) != 0 :
                inconsistent_FeatureTypes_multiplicity.append((FC_name,FC_Attributes_lst,FC_Multiplicity_lst,DCEG_Multiplicity_lst))

            if not FC_permittedValues_lst == DCEG_permittedValues_lst:
                inconsistent_FeatureTypes_permittedValues.append((FC_name,FC_Enumerates_lst,FC_permittedValues_lst,DCEG_permittedValues_lst))

        else:
            omission_FeatureTypes_DCEG.append(FC_name) 
        

    #__________Cohérence titre / sous-titre DCEG__________
    for chap_DCEG in DCEG_chap_lst:
        FeatureType_DCEG_dict = FeatureTypes_DCEG_dict[chap_DCEG]
        title_DCEG = FeatureType_DCEG_dict['titre']
        if '§1' in FeatureType_DCEG_dict.keys():
            if title_DCEG != "drawing instruction": # Permet de ne pas considérer "drawing instruction" qui est en fait un attribut"
                if 'IHO Definition:' in FeatureType_DCEG_dict['§1']:
                    subtitle_DCEG_1 = FeatureType_DCEG_dict['§1'].split('IHO Definition: ')[1].split('.')[0]
                    
                    i = 2
                    para_num = '§'+str(i)
                    while FeatureType_DCEG_dict[para_num][:5] != 'S-101':
                        i+=1
                        para_num = '§'+str(i)
                    subtitle_DCEG_2 = FeatureType_DCEG_dict[para_num].split(': ')[1].split(' (')[0]
                        
                    if not title_DCEG.lower() == subtitle_DCEG_1.lower() or not title_DCEG.lower() == subtitle_DCEG_2.lower():
                        inconsistent_FeatureTypes_DCEG_title.append((title_DCEG,subtitle_DCEG_1,subtitle_DCEG_2))
                    
    return(omission_FeatureTypes_DCEG,
           inconsistent_FeatureTypes_DCEG_title,
           inconsistent_FeatureTypes_definition,
           omission_FeatureTypes_definition_DCEG,
           inconsistent_FeatureTypes_alias,
           omission_FeatureTypes_alias_DCEG,
           inconsistent_FeatureTypes_attributes,
           inconsistent_FeatureTypes_multiplicity,
           FeatureTypes_multiplicity_error,
           inconsistent_FeatureTypes_permittedValues)