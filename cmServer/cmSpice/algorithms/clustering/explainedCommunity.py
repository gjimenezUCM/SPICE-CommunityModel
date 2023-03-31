import numpy as np
import statistics

import pandas as pd

import json

# ---------logger---------

from cmSpice.logger.logger import getLogger

logger = getLogger(__name__)
# ------------------------

def getMostFrequentElementsList(array, k):
    df = pd.DataFrame({'Number': array, 'Value': array})
    df['Count'] = df.groupby(['Number'])['Value'].transform('count')

    df1 = df.copy()
    df1 = df1.sort_values(by=['Count'], ascending=False)
    df1 = df1.drop_duplicates(['Number'])

    return df1.head(k)[['Number', 'Count']].to_dict('records')

def explainInteractionAttributes(perspective):
    return len(perspective['interaction_similarity_functions']) > 0

def getCommunity(explainedObject, id_community, answer_binary, percentage, daoAPI_iconclass):
    """Method to obtain all information about a community.

    Args:
        id_community (int): Id or name of community returned by detection method.
        answer_binary (bool, optional): True to indicate that a common property
        occurs only when all answers are 1.0. Defaults to False. Defaults to False.

    Returns:
        dict: All data that describes the community:
            - name: name of community.
            - members: list of index included in this community.
            - properties: common properties of community. It is a dictionary where:
                each property is identified by column_name of data, and the value is
                the common value in this column.
    """
    try:

        # print("get community: " + str(id_community))

        community = explainedObject.communities.get_group(id_community)
        # community = explainedObject.simplifyInteractionAttributes(community, printing = False)

        community_user_attributes = community[explainedObject.user_attributes]

        community_data = {'name': id_community}
        community_data['percentage'] = str(percentage * 100) + " %"
        # community_data['members'] = list(community_user_attributes.index.values)
        community_data['members'] = community['userid'].tolist()

        community_data['data'] = community

        explainedCommunityProperties = dict()

        # for col in community.columns.values:
        # for col2 in explainedObject.explanaible_attributes:
        for col2 in explainedObject.explanaible_attributes + explainedObject.artwork_attributes:
            if col2 != 'community':
                if explainInteractionAttributes(explainedObject.perspective):
                    col = "community_" + col2
                else:
                    col = col2
                # print(community)
                # print(len(community[col]))
                # print('-', col, community[col].value_counts().index[0])
                if answer_binary:
                    if (len(community[col]) * percentage) <= community[col].sum():
                        explainedCommunityProperties[col] = community[col].value_counts().index[0]

                        # print('-', col, community[col].value_counts().index[0])
                else:

                    array = community[col].tolist()
                    # For iconclass (list) types
                    # if (len(community[col] > 0 and isinstance(community[col][0],list))):

                    # Generic for dict types (iconclass, ontology, artwork id)
                    if len(array) > 0 and isinstance(array[0], dict):
                        explainedCommunityProperties = __get_community_genericDict(explainedObject, id_community, array, col,
                                                                                        col2,
                                                                                        explainedCommunityProperties, daoAPI_iconclass)

                    # For iconclass
                    elif col == ("community_" + "iconclassArrayIDs"):
                        explainedCommunityProperties = __get_community_iconClass(explainedObject, array, col, col2,
                                                                                      explainedCommunityProperties, daoAPI_iconclass)

                    # For materials ontology
                    elif col == ("community_" + "Materials") and 1 == 1:
                        explainedCommunityProperties = __get_community_materialOntology(explainedObject, array, col, col2,
                                                                                             explainedCommunityProperties)

                    # For id
                    elif col == ("community_" + "id") and 1 == 1:
                        explainedCommunityProperties = __get_community_id(explainedObject, array, col, col2,
                                                                               explainedCommunityProperties)

                    # For list types (artworks and iconclass)
                    elif len(array) > 0 and isinstance(array[0], list):
                        explainedCommunityProperties = __get_community_listTypes(explainedObject, array, col, col2,
                                                                                      explainedCommunityProperties, daoAPI_iconclass)

                    # For string types
                    else:
                        explainedCommunityProperties = __get_community_stringTypes(explainedObject, col, col2,
                                                                                        explainedCommunityProperties,
                                                                                        community)

        # Second explanation


        community_data['explanation'] = explainedCommunityProperties

        # community_data['explanation'].append(__secondExplanation(community))

    except Exception as e:

        logger.error(str(e))
        logger.error(explainedObject.communities)
        # data with communities
        logger.error(explainedObject.complete_data)
        logger.error("\n\n")
        logger.error("algorithm result")
        logger.error(explainedObject.resultAlgorithm)
        logger.error(explainedObject.idsCommunities)
        logger.error("\n")
        raise Exception("Exception retrieving community " + str(id_community))
        # return -1

    return community_data


def __get_community_genericDict(explainedObject, id_community, array, col, col2, explainedCommunityProperties, daoAPI_iconclass):
    logger.info("improved explanation for dict type explanations")
    logger.info("col: " + str(col))
    logger.info("\n")

    logger.info(array)
    logger.info("\n")

    logger.info("end new dict type explanations")
    logger.info("\n")

    # Example array
    # [{}, {'31D1': [['31D15', '31D12']]}] (iconclass)
    #
    # {'44174': ['44174']} (id)

    # Combine all dictionaries inside the array into one dictionary
    iconclassDictionary = {}
    for dictionary in array:
        for dictionaryKey in dictionary:
            if dictionaryKey not in iconclassDictionary:
                iconclassDictionary[dictionaryKey] = []
            iconclassDictionary[dictionaryKey].extend(dictionary[dictionaryKey])

    if col != ("community_" + "id"):
        for key in iconclassDictionary:
            logger.info("iconclassDictionary " + "(" + str(key) + ")")
            logger.info(iconclassDictionary[key])

            set_of_jsons = {json.dumps(d, sort_keys=True) for d in iconclassDictionary[key]}
            iconclassDictionary[key] = [json.loads(t) for t in set_of_jsons]

            logger.info(iconclassDictionary[key])
            logger.info("\n")
            """
            """

    # Sort dictionary
    result2 = __sortDictionary(iconclassDictionary)

    result3 = {}

    logger.info("community: " + str(id_community))
    logger.info("iconclassDictionary explanation")
    logger.info(iconclassDictionary)
    logger.info("\n")
    logger.info("result2 explanation")
    logger.info(result2)
    logger.info("\n")

    # Prepare explanation text for each of the selected keys
    for iconclassID in result2:
        logger.info("checking iconclass id " + str(iconclassID))
        iconclassText = ""
        if col == "community_" + "iconclassArrayIDs":
            iconclassText = daoAPI_iconclass.getIconclassText(iconclassID)

        # Get array of dicts {key: iconclassID, value: artwork it originates from}
        np_array = np.asarray(result2[iconclassID], dtype=object)
        iconclassChildren = list(np.hstack(np_array))

        logger.info("iconclass children")
        logger.info(iconclassChildren)
        logger.info("\n")

        # basic explanation
        # iconclassExplanation = str(iconclassID) + " " + iconclassText
        iconclassExplanation = iconclassText + " " + "[" + str(iconclassID) + "]"
        artworksExplanation = []

        # key includes children keys (dict value): iconclass, ontology
        if isinstance(iconclassChildren[0], dict):

            # Group iconclassChildren into a combined dictionary (values with the same key are added to an array)
            iconclassChildrenCombinedDictionary = __groupIconclassChildrenCombinedDictionary(iconclassChildren)

            if iconclassID in iconclassChildrenCombinedDictionary:
                iconclassExplanation += " (" + ", ".join(
                    iconclassChildrenCombinedDictionary[iconclassID]) + ")"
                artworksExplanation.extend(iconclassChildrenCombinedDictionary[iconclassID])
            iconclassChildrenText = []
            if len(iconclassChildrenCombinedDictionary) > 1:
                logger.info("iconclass combined dictionary")
                logger.info(iconclassChildrenCombinedDictionary)
                logger.info("\n")

                # iconclassExplanation += ". Obtained from the artwork's materials: "
                iconclassExplanation += ". Obtained from the artwork's " + str(
                    col2).lower() + ": "
                for iconclassChild in iconclassChildrenCombinedDictionary:
                    iconclassChildText = ""
                    # Iconclass: Get description of the iconclassID through the Iconclass API
                    if col == ("community_" + "iconclassArrayIDs"):
                        iconclassChildText = daoAPI_iconclass.getIconclassText(
                            iconclassChild)
                    iconclassChildText += " (" + ", ".join(
                        iconclassChildrenCombinedDictionary[iconclassChild]) + ")"
                    artworksExplanation.extend(
                        iconclassChildrenCombinedDictionary[iconclassChild])
                    # iconclassChildrenText.append(str(iconclassChild) + " " + iconclassChildText)
                    iconclassChildrenText.append(
                        iconclassChildText + " " + "[" + str(iconclassChild) + "]")
                iconclassExplanation += "; ".join(iconclassChildrenText)
                iconclassExplanation += ""

        # key references a basic array value: artwork id
        else:

            iconclassChildren = list(set(iconclassChildren))
            iconclassChildrenCombinedDictionary = {iconclassChildren[0]: iconclassChildren}
            artworksExplanation.extend(iconclassChildrenCombinedDictionary[iconclassID])
            # iconclassChildren = {}

        logger.info("iconclass children combined")
        logger.info(iconclassChildrenCombinedDictionary)
        logger.info("\n")

        # result3[iconclassExplanation] = 0.0
        result3[iconclassExplanation] = list(set(artworksExplanation))

    return __setExplainedCommunityProperties(explainedCommunityProperties, result3, col, col2)


def __get_community_iconClass(explainedObject, array, col, col2, explainedCommunityProperties, daoAPI_iconclass):
    logger.info("improved explanation for iconclass")
    logger.info("\n")

    logger.info(array)
    logger.info("\n")

    logger.info("end new iconclass")
    logger.info("\n")

    # Example array
    # [{}, {'31D1': [['31D15', '31D12']]}]

    # Combine all into one dictionary
    iconclassDictionary = __combineIconclassDictionary(array)

    # Sort dictionary
    result2 = explainedObject.__sortDictionary(iconclassDictionary)

    result3 = {}
    for iconclassID in result2:
        iconclassText = daoAPI_iconclass.getIconclassText(iconclassID)
        # Get array of dicts {key: iconclassID, value: artwork it originates from}
        iconclassExplanation, iconclassChildrenCombinedDictionary = __getArrayOfDicts(result2, iconclassID,
                                                                                           iconclassText)

        iconclassChildrenText = []

        if len(iconclassChildrenCombinedDictionary) > 1:
            logger.info("iconclass combined dictionary")
            logger.info(iconclassChildrenCombinedDictionary)
            logger.info("\n")

            iconclassExplanation += ". Obtained from the artwork's iconclass IDs: "
            for iconclassChild in iconclassChildrenCombinedDictionary:
                iconclassChildText = daoAPI_iconclass.getIconclassText(iconclassChild)
                iconclassChildText += " (" + ", ".join(
                    iconclassChildrenCombinedDictionary[iconclassChild]) + ")"
                iconclassChildrenText.append(str(iconclassChild) + " " + iconclassChildText)
            iconclassExplanation += "; ".join(iconclassChildrenText)
            iconclassExplanation += ""

        result3[iconclassExplanation] = 0.0

    return __setExplainedCommunityProperties(explainedCommunityProperties, result3, col, col2)


def __get_community_materialOntology(explainedObject, array, col, col2, explainedCommunityProperties):
    logger.info("improved explanation for materials")
    logger.info("\n")

    logger.info(array)
    logger.info("\n")

    logger.info("end new materials")
    logger.info("\n")

    # Example array
    # [{}, {'31D1': [['31D15', '31D12']]}]

    # Combine all into one dictionary
    iconclassDictionary = __combineIconclassDictionary(array)

    # Sort dictionary
    result2 = __sortDictionary(iconclassDictionary)

    result3 = {}
    for iconclassID in result2:
        iconclassText = ""
        # Get array of dicts {key: iconclassID, value: artwork it originates from}
        iconclassExplanation, iconclassChildrenCombinedDictionary = __getArrayOfDicts(result2, iconclassID,
                                                                                           iconclassText)

        iconclassChildrenText = []
        if len(iconclassChildrenCombinedDictionary) > 1:
            logger.info("iconclass combined dictionary")
            logger.info(iconclassChildrenCombinedDictionary)
            logger.info("\n")

            iconclassExplanation = __setIconclassExplanation(iconclassExplanation,
                                                                  iconclassChildrenCombinedDictionary,
                                                                  iconclassChildrenText)

        result3[iconclassExplanation] = 0.0

    return __setExplainedCommunityProperties(explainedCommunityProperties, result3, col, col2)


def __get_community_id(explainedObject, array, col, col2, explainedCommunityProperties):
    # Example array
    # [{}, {'31D1': [['31D15', '31D12']]}]

    # Combine all into one dictionary
    iconclassDictionary = {}
    for dictionary in array:
        for dictionaryKey in dictionary:
            if dictionaryKey not in iconclassDictionary:
                iconclassDictionary[dictionaryKey] = []
            iconclassDictionary[dictionaryKey].extend(dictionary[dictionaryKey])

    # Sort dictionary
    result2 = __sortDictionary(iconclassDictionary)

    result3 = {}
    for iconclassID in result2:
        iconclassText = ""
        # Get array of dicts {key: iconclassID, value: artwork it originates from}
        np_array = np.asarray(result2[iconclassID], dtype=object)
        iconclassChildren = list(np.hstack(np_array))

        iconclassExplanation = str(iconclassID) + " " + iconclassText

        if isinstance(iconclassChildren[0], dict):
            # Group iconclassChildren into a combined dictionary (values with the same key are added to an array)
            iconclassChildrenCombinedDictionary = __groupIconclassChildrenCombinedDictionary(iconclassChildren)

            if iconclassID in iconclassChildrenCombinedDictionary:
                iconclassExplanation += " (" + ", ".join(
                    iconclassChildrenCombinedDictionary[iconclassID]) + ")"
                iconclassChildrenText = []
                if len(iconclassChildrenCombinedDictionary) > 1:
                    iconclassExplanation = __setIconclassExplanation(iconclassExplanation,
                                                                          iconclassChildrenCombinedDictionary,
                                                                          iconclassChildrenText)

        else:
            iconclassChildren = list(set(iconclassChildren))
            iconclassChildrenCombinedDictionary = {iconclassChildren[0]: iconclassChildren}

            # iconclassChildren = {}

        # result3[iconclassExplanation] = 0.0
        result3[iconclassExplanation] = iconclassChildrenCombinedDictionary[iconclassID]

    return __setExplainedCommunityProperties(explainedCommunityProperties, result3, col, col2)


def __get_community_listTypes(explainedObject, array, col, col2, explainedCommunityProperties, daoAPI_iconclass):
    np_array = np.asarray(array, dtype=object)

    # array2 = list(np_array.flat)
    array2 = list(np.hstack(np_array))

    # logger.info("array2: " + str(array2))


    result = getMostFrequentElementsList(array2, 5)
    result = [x['Number'] for x in result]

    result2 = {}

    logger.info("before entering iconclass extra functionality")
    logger.info(col)
    logger.info("\n")

    # Iconclass attribute
    if col == "community_" + "iconclassArrayIDs":
        for iconclassID in result:
            iconclassText = daoAPI_iconclass.getIconclassText(iconclassID)
            result2[str(iconclassID) + " " + iconclassText] = 0.0
    # Other array attributes
    else:
        for element in result:
            result2[str(element)] = 0.0

    # result2.append(str(array) + " " + "0.0")

    logger.info("result2: " + str(result2))

    # explainedCommunityProperties[col] = "\n".join(result2)

    explainedCommunityProperties[col] = dict()
    explainedCommunityProperties[col][
        "label"] = 'Community representative properties of the implicit attribute ' + "(" + str(
        col2) + ")" + ":"
    explainedCommunityProperties[col]["explanation"] = result2

    return explainedCommunityProperties


def __get_community_stringTypes(explainedObject, col, col2, explainedCommunityProperties, community):
    # explainableAttribute = __is_explainable(community, answer_binary, percentage)

    # Returns dominant one
    # explainedCommunityProperties[col] = community[col].value_counts().index[0]

    # Remove empty string
    df = community.copy()
    df2 = df.loc[df[col].str.len() != 0]
    percentageColumn = df2[col].value_counts(normalize=True) * 100
    percentageColumnDict = percentageColumn.to_dict()

    # Returns the values for each of them
    """
    percentageColumn = community[col].value_counts(normalize=True) * 100
    percentageColumnDict = percentageColumn.to_dict()
    """

    explainedCommunityProperties[col] = dict()
    explainedCommunityProperties[col][
        "label"] = 'Percentage distribution of the implicit attribute ' + "(" + str(
        col2) + ")" + ":"
    # if (not explainableAttribute):
    # explainedCommunityProperties[col]["label"] += "(This community doesn't meet the dissimilar requirements) :"
    # explainedCommunityProperties[col]["label"] += "distanceCommunity: " + str(distanceCommunity)
    explainedCommunityProperties[col]["explanation"] = percentageColumnDict

    return explainedCommunityProperties


def __getArrayOfDicts(explainedObject, result2, iconclassID, iconclassText):
    np_array = np.asarray(result2[iconclassID], dtype=object)
    iconclassChildren = list(np.hstack(np_array))

    logger.info("iconclass children")
    logger.info(iconclassChildren)
    logger.info("\n")

    # Group iconclassChildren into a combined dictionary (values with the same key are added to an array)
    iconclassChildrenCombinedDictionary = __groupIconclassChildrenCombinedDictionary(iconclassChildren)

    logger.info("iconclass children combined")
    logger.info(iconclassChildrenCombinedDictionary)
    logger.info("\n")

    iconclassExplanation = str(iconclassID) + " " + iconclassText
    if iconclassID in iconclassChildrenCombinedDictionary:
        iconclassExplanation += " (" + ", ".join(
            iconclassChildrenCombinedDictionary[iconclassID]) + ")"

    return iconclassExplanation, iconclassChildrenCombinedDictionary


def __setExplainedCommunityProperties(explainedObject, explainedCommunityProperties, result3, col, col2):
    logger.info("result3: " + str(result3))

    # explainedCommunityProperties[col] = "\n".join(result2)

    explainedCommunityProperties[col] = dict()
    explainedCommunityProperties[col][
        "label"] = 'Community representative properties of the implicit attribute ' + "(" + str(
        col2) + ")" + ":"
    explainedCommunityProperties[col]["explanation"] = result3

    return explainedCommunityProperties


def __setIconclassExplanation(explainedObject, iconclassExplanation, iconclassChildrenCombinedDictionary,
                              iconclassChildrenText):
    iconclassExplanation += ". Obtained from the artwork's materials: "
    for iconclassChild in iconclassChildrenCombinedDictionary:
        iconclassChildText = ""
        iconclassChildText += " (" + ", ".join(
            iconclassChildrenCombinedDictionary[iconclassChild]) + ")"
        iconclassChildrenText.append(str(iconclassChild) + " " + iconclassChildText)
    iconclassExplanation += "; ".join(iconclassChildrenText)
    iconclassExplanation += ""
    return iconclassExplanation


def __sortDictionary(explainedObject, iconclassDictionary):
    # Sort dictionary
    res = '#separator#'.join(
        sorted(iconclassDictionary, key=lambda key: len(iconclassDictionary[key])))
    result = res.split('#separator#')
    result.reverse()

    # Get x more frequent keys
    result2 = []
    result2 = {k: iconclassDictionary[k] for k in result[0:5:1] if k in iconclassDictionary}

    return result2


def __groupIconclassChildrenCombinedDictionary(explainedObject, iconclassChildren):
    iconclassChildrenCombinedDictionary = {}
    for dictionary in iconclassChildren:
        for key, value in dictionary.items():
            if key not in iconclassChildrenCombinedDictionary:
                iconclassChildrenCombinedDictionary[key] = []
            iconclassChildrenCombinedDictionary[key].extend(value)
            iconclassChildrenCombinedDictionary[key] = list(
                set(iconclassChildrenCombinedDictionary[key]))
    return iconclassChildrenCombinedDictionary


def __combineIconclassDictionary(explainedObject, array):
    iconclassDictionary = {}
    for dictionary in array:
        for dictionaryKey in dictionary:
            if dictionaryKey not in iconclassDictionary:
                iconclassDictionary[dictionaryKey] = []
            iconclassDictionary[dictionaryKey].extend(dictionary[dictionaryKey])
    return iconclassDictionary
