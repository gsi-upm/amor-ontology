from pydantic import BaseModel, Field
from fastapi import Query
from typing import List, Optional, Union
from enum import Enum
from datetime import datetime


class Label(BaseModel):
    language: str = Field(..., alias="@language")
    value: str = Field(..., alias="@value")

class Answer(BaseModel):
    text: str = Field(..., alias="schema:text")
    #answer_type: Optional[str] = Field(..., alias="@type")

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
    type: List[str] = Field(..., alias="@type")
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
    hasAccesibilityCategory: str = Field(..., alias="amor-exp:hasAccesibilityCategory")
    hasAgeBracket: str = Field(..., alias="amor-exp:hasAgeBracket")
    hasAverageSocialNetworkActivityPerMonth: int = Field(..., alias="amor-exp:hasAverageSocialNetworkActivityPerMonth")
    hasEducationLevel: str = Field(..., alias="amor-exp:hasEducationLevel")
    hasNumberOfFollowers: int = Field(..., alias="amor-exp:hasNumberOfFollowers")
    hasPoliticalOrientation: str = Field(..., alias="amor-exp:hasPoliticalOrientation")
    hasPreferredContent: List[str] = Field(..., alias="amor-exp:hasPreferredContent")
    hasPreferredEntity: List[str] = Field(..., alias="amor-exp:hasPreferredEntity")
    hasPreferredTopic: List[str] = Field(..., alias="amor-exp:hasPreferredTopic")
    hasStressLevel: float = Field(..., alias="amor-exp:hasStressLevel")
    hasMoralProfile: MoralProfile = Field(..., alias="amor:hasMoralProfile")
    rdfs_label: Label = Field(..., alias="rdfs:label")
    foaf_gender: str = Field(..., alias="foaf:gender")


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

class Dataset(BaseModel):
    did: str = Field(alias="@id")
    dtype: Optional[str] = Field(alias="@type")
    url: Optional[str] = Field(alias="schema:url")


class Experiment(BaseModel):
    hasBackgroundMusic: Optional[str] = Field(..., alias="amor-exp:hasBackgroundMusic")
    hasBackgroundScenario: Optional[str] = Field(..., alias="amor-exp:hasBackgroundScenario")
    hasContentAdaptationStrategy: List[ContentAdaptationStrategy] = Field(..., alias="amor-exp:hasContentAdaptationStrategy")
    hasExecutor: Optional[Union[Executor, str]] = Field(..., alias="amor-exp:hasExecutor")
    hasExperimentEvaluation: ExperimentEvaluation = Field(..., alias="amor-exp:hasExperimentEvaluation")
    hasExperimentationSubject: ExperimentationSubject = Field(..., alias="amor-exp:hasExperimentationSubject")
    hasLLMConfiguration: LLMConfiguration = Field(..., alias="amor-exp:hasLLMConfiguration")
    hasPhysicalMovement: Optional[List[str]] = Field(..., alias="amor-exp:hasPhysicalMovement")
    hasRequester: Entity = Field(..., alias="amor-exp:hasRequester")
    hasVisualizationStrategy: Optional[List[VisualizationStrategy]] = Field(..., alias="amor-exp:hasVisualizationStrategy")
    usesAggregatedData: str = Field(..., alias="amor-exp:usesAggregatedData")
    usesAvatar: Avatar = Field(..., alias="amor-exp:usesAvatar")
    usesDataset: Union[str, Dataset] = Field(..., alias="amor-exp:usesDataset")
    usesEmotionRecognitionCooperationStrategy: EmotionRecognitionCooperationStrategy = Field(..., alias="amor-exp:usesEmotionRecognitionCooperationStrategy")
    usesLanguage: str = Field(..., alias="amor-exp:usesLanguage")
    usesRobotCooperationStrategy: Optional[RobotCooperationStrategy] = Field(..., alias="amor-exp:usesRobotCooperationStrategy")
    usesSemanticCooperationStrategy: Optional[SemanticCooperationStrategy] = Field(..., alias="amor-exp:usesSemanticCooperationStrategy")
