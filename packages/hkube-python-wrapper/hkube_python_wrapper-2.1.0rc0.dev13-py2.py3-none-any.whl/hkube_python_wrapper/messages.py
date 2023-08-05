from __future__ import print_function, division, absolute_import

outgoing = {
    "initialized": "initialized",
    "started": "started",
    "stopped": "stopped",
    "progress": "progress",
    "error": "errorMessage",
    "storing": "storing",
    "done": "done",
    "startAlgorithmExecution": "startAlgorithmExecution",
    "stopAlgorithmExecution": "stopAlgorithmExecution",
    "startRawSubPipeline": "startRawSubPipeline",
    "startStoredSubPipeline": "startStoredSubPipeline",
    "stopSubPipeline": "stopSubPipeline"

}
incoming = dict(initialize="initialize", start="start", stop="stop", algorithmExecutionError="algorithmExecutionError",
                algorithmExecutionDone="algorithmExecutionDone", subPipelineStarted="subPipelineStarted",
                subPipelineError="subPipelineError", subPipelineDone="subPipelineDone",
                subPipelineStopped="subPipelineStopped")
