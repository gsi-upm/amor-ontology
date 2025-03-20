from pydantic import BaseModel
from pydantic import Field, GetCoreSchemaHandler, GetJsonSchemaHandler, model_validator
from pydantic_core import CoreSchema, core_schema
from fastapi import Query
from typing import List, Optional, Union, Any, Type
from collections.abc import Callable, Iterator
from enum import Enum
from datetime import datetime

import uuid


def new_id():
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, 'www.gsi.upm.es'))

class Label(BaseModel):
    language: str = Field(..., alias="@language")
    value: str = Field(..., alias="@value")


class Answer(BaseModel):
    text: str = Field(..., alias="schema:text")
    # answer_type: Optional[str] = Field(..., alias="@type")


class Question(BaseModel):
    text: Label = Field(..., alias="schema:text")
    atype: Optional[str] = Field(..., alias="@type")
    options: Optional[List[Answer]] = Field(None, alias="schema:suggestedAnswer")


class ExperimentEvaluation(BaseModel):
    hasFinalQuestion: Optional[Question] = Field(..., alias="amor-exp:hasFinalQuestion")
    hasInitialQuestion: Optional[List[Question]] = Field(..., alias="amor-exp:hasInitialQuestion")
    hasIntermediateQuestion: Optional[Question] = Field(..., alias="amor-exp:hasIntermediateQuestion")


class Executor(BaseModel):
    id: str = Field(..., alias="@id")
    type: List[str] = Field(default=["Executor", ], alias="@type")
    label: Label = Field(..., alias="rdfs:label")


class MoralValueAnnotation(BaseModel):
    type: str = Field(..., alias="@type")
    bias: float = Field(..., alias="amor-mft:hasBias")
    category: str = Field(..., alias="amor:hasMoralValueCategory")
    label: Label = Field(..., alias="rdfs:label")


class MoralProfile(BaseModel):
    type: str = Field(..., alias="@type")
    analysed: dict = Field(..., alias="amor:analysed")
    model: str = Field(..., alias="amor:usedMoralValueModel")
    label: Label = Field(..., alias="rdfs:label")
    endedAtTime: datetime = Field(..., alias="prov:endedAtTime")
    generated: Optional[List[Union[Executor, MoralValueAnnotation]]] = None


class ExperimentationSubject(BaseModel):
    hasAccesibilityCategory: Optional[str] = Field(default=None, alias="amor-exp:hasAccesibilityCategory")
    hasAgeBracket: Optional[str] = Field(default=None, alias="amor-exp:hasAgeBracket")
    hasAverageSocialNetworkActivityPerMonth: Optional[int] = Field(default=None, alias="amor-exp:hasAverageSocialNetworkActivityPerMonth")
    hasEducationLevel: Optional[str] = Field(default=None, alias="amor-exp:hasEducationLevel")
    hasNumberOfFollowers: Optional[int] = Field(default=None, alias="amor-exp:hasNumberOfFollowers")
    hasPoliticalOrientation: Optional[str] = Field(default=None, alias="amor-exp:hasPoliticalOrientation")
    hasPreferredContent: Optional[List[str]] = Field(default=[], alias="amor-exp:hasPreferredContent")
    hasPreferredEntity: Optional[List[str]] = Field(default=[], alias="amor-exp:hasPreferredEntity")
    hasPreferredTopic: Optional[List[str]] = Field(default=[], alias="amor-exp:hasPreferredTopic")
    hasStressLevel: Optional[float] = Field(default=None, alias="amor-exp:hasStressLevel")
    hasMoralProfile: Optional[MoralProfile] = Field(default=None, alias="amor:hasMoralProfile")
    rdfs_label: Optional[Label] = Field(default=None, alias="rdfs:label")
    foaf_gender: Optional[str] = Field(default=None, alias="foaf:gender")


class Avatar(BaseModel):
    hasAppearance: List[str] = Field(..., alias="amor-exp:hasAppearance")
    hasCategory: str = Field(..., alias="amor-exp:hasCategory")
    hasFacialExpresivity: str = Field(..., alias="amor-exp:hasFacialExpresivity")
    hasGesturalExpresivity: str = Field(..., alias="amor-exp:hasGesturalExpresivity")
    hasLanguageComplexityLevel: str = Field(..., alias="amor-exp:hasLanguageComplexityLevel")
    hasPersonality: str = Field(..., alias="amor-exp:hasPersonality")
    hasVocalExpresivity: str = Field(..., alias="amor-exp:hasVocalExpresivity")
    foaf_age: int = Field(..., alias="foaf:age")
    foaf_gender: str = Field(..., alias="foaf:gender")


class LLMConfiguration(BaseModel):
    hasLLMModel: str = Field(..., alias="amor-exp:hasLLMModel")
    hasLLMToken: str = Field(..., alias="amor-exp:hasLLMToken")
    usesLLMEndPoint: str = Field(..., alias="amor-exp:usesLLMEndPoint")
    usesLLMService: str = Field(..., alias="amor-exp:usesLLMService")
    usesPrompt: str = Field(..., alias="amor-exp:usesPrompt")


class Entity(BaseModel):
    eid: str = Field(alias="@id")
    label: Label = Field(alias="rdfs:label")


class EmotionRecognitionCooperationStrategy(str, Enum):
    NO_COOPERATION = "amor-exp:NoCooperationEmotionRecognition"
    FULL_COOPERATION = "amor-exp:FullCooperationEmotionRecognition"
    LOCAL_COOPERATION = "amor-exp:LocalEmotionRecognition"
    CLOUD_COOPERATION = "amor-exp:CloudEmotionRecognition"


# Semantic Cooperation Strategies Enum
class SemanticCooperationStrategy(str, Enum):
    FULL_SEMANTIC_COOPERATION = "amor-exp:FullSemanticCooperation"
    LOCAL_EMOTION_RECOGNITION = "amor-exp:LocalEmotionRecognition"


class SemanticCooperationConfiguration(BaseModel):
    strategy: SemanticCooperationStrategy = Field(..., alias="amor-exp:usesSemanticCooperationStrategy")
    sparqlQuery: Optional[List[str]] = Field(..., alias="amor-exp:usesSPARQLQuery")
    cloudGraphQuery: Optional[List[str]] = Field(..., alias="amor-exp:usesCloudGraphQuery")


# Visualization Strategies Enum
class VisualizationStrategy(str, Enum):
    MORAL_VALUE = "amor-exp:MoralValueVisualizationStrategy"
    AFFECTIVE_VALUE = "amor-exp:AffectiveValueVisualizationStrategy"
    CLICK_BAIT = "amor-exp:ClickBaitVisualizationStrategy"
    FAKE_NEWS = "amor-exp:FakeNewsVisualizationStrategy"


# Content Adaptation Strategies Enum
class ContentAdaptationStrategy(str, Enum):
    MORAL_ADAPTATION_STRATEGY = "amor-exp:MoralAdaptationStrategy"
    AFFECTIVE_ADAPTATION_STRATEGY = "amor-exp:AfectiveAdaptationStrategy"


# Robot Cooperation Strategies Enum
class RobotCooperationStrategy(str, Enum):
    NO_COOPERATION_ROBOT = "amor-exp:NoCooperationRobot"
    COOPERATIVE_ROBOT = "amor-exp:CooperativeRobot"
    COMPETITIVE_ROBOT = "amor-exp:CompetitiveRobot"


class RobotCooperationConfiguration(BaseModel):
    strategy: RobotCooperationStrategy = Field(..., alias="usesRobotCooperationStrategy")
    roleType: str = Field(..., alias="hasRobotRole")


class Dataset(BaseModel):
    did: str = Field(alias="@id")
    dtype: Optional[str] = Field(alias="@type")
    url: Optional[str] = Field(alias="schema:url")


class ExperimentConfiguration(BaseModel):
    hasBackgroundMusic: Optional[str] = Field(None, alias="amor-exp:hasBackgroundMusic")
    hasBackgroundScenario: Optional[str] = Field(None, alias="amor-exp:hasBackgroundScenario")
    hasExecutor: Optional[Union[str, Executor]] = Field(None, alias="amor-exp:hasExecutor")
    hasExperimentEvaluation: ExperimentEvaluation = Field(None, alias="amor-exp:hasExperimentEvaluation")
    hasExperimentationSubject: ExperimentationSubject = Field(None, alias="amor-exp:hasExperimentationSubject")
    hasLLMConfiguration: Optional[LLMConfiguration] = Field(None, alias="amor-exp:hasLLMConfiguration")
    hasPhysicalMovement: Optional[List[str]] = Field(None, alias="amor-exp:hasPhysicalMovement")
    hasRequester: Optional[Entity] = Field(None, alias="amor-exp:hasRequester")
    usesAggregatedData: Optional[str] = Field(None, alias="amor-exp:usesAggregatedData")
    usesAvatar: Optional[Avatar] = Field(None, alias="amor-exp:usesAvatar")
    usesDataset: Optional[Union[str, Dataset]] = Field(None, alias="amor-exp:usesDataset")
    usesLanguage: Optional[str] = Field(None, alias="amor-exp:usesLanguage")
    hasContentAdaptationStrategy: Optional[List[ContentAdaptationStrategy]] = Field(None, alias="amor-exp:hasContentAdaptationStrategy")
    hasVisualizationStrategy: Optional[List[VisualizationStrategy]] = Field(None, alias="amor-exp:hasVisualizationConfiguration")
    usesEmotionRecognitionCooperationStrategy: Optional[EmotionRecognitionCooperationStrategy] = Field(None, alias="amor-exp:usesEmotionRecognitionCooperationStrategy")

    usesRobotCooperationConfiguration: Optional[RobotCooperationConfiguration] = Field(None, alias="amor-exp:usesRobotCooperationConfiguration")
    usesSemanticCooperationConfiguration: Optional[SemanticCooperationConfiguration] = Field(None, alias="amor-exp:usesSemanticCooperationConfiguration")

class Experiment(ExperimentConfiguration):
    id: str = Field(..., serialization_alias="@id")
