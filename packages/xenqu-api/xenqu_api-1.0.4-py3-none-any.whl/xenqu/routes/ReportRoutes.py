from xenqu._XenquBase import XenquBase

_prefix = '/reporting'

class ReportRoutes:

    base: XenquBase

    def __init__(self, base: XenquBase) -> None:
        self.base = base


    """
    * Get Report Results

    Parameters
    ----------
        jobId: str
            job ID for report runs

        status: int
            status of the results to retrieve

        count: int
            number of results to return

        offset: int
            offset of the results

        sortByAsc: bool = True
            sorting of results

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#c5b6a594-36a3-4285-a60c-2580dd0e40a5}
    """
    def getReportResults(self, jobId: str, status: int, count: int, offset: int, sortByAsc: bool = True):
        params = {
            "job_id": jobId,
            "status": status,
            "count": count,
            "offset": offset
        }

        if sortByAsc:
            params["sortby"] = "run_date:asc"
        else:
            params["sortby"] = "run_date:dec"

        data = self.base.makeGet(f"{_prefix}/results/", parameters=params)
        return data


    """
    * Get Report Result

    Parameters
    ----------
        reportId: str
            ID of the specific report to retrieve

    ? @see [API Docs]{@link https://apidocs.xenqu.com/#94d68fc1-e80a-46e5-a4e9-dbef2c562d69}
    """
    def getReportResult(self, reportId: str):
        data = self.base.makeGet(f"{_prefix}/results/{reportId}")
        return data
