# This file is part of ctrl_bps.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""API for cancelling runs submitted to a WMS.
"""

import logging

from lsst.utils import doImport


_LOG = logging.getLogger(__name__)


def cancel(wms_service, wms_id=None, run=None, user=None, require_bps=True, pass_thru=None):
    """Cancel submitted workflows.

    Parameters
    ----------
    wms_service : `str` or `lsst.ctrl.bps.BaseWmsService`
        Name of the Workload Management System service class.
    wms_id : `str`, optional
        ID or path of job that should be canceled.
    run : `str`, optional
        Run name (Run collection with / replaced with _).
    user : `str`, optional
        User whose submitted jobs should be canceled.
    require_bps : `bool`, optional
        Whether to require given run_id/user to be a bps submitted job.
    pass_thru : `str`, optional
        Information to pass through to WMS.
    """
    _LOG.debug("Cancel params: wms_id=%s, run=%s, user=%s, require_bps=%s, pass_thru=%s",
               wms_id, run, user, require_bps, pass_thru)

    if isinstance(wms_service, str):
        wms_service_class = doImport(wms_service)
        service = wms_service_class({})
    else:
        service = wms_service

    jobs = service.list_submitted_jobs(wms_id, run, user, require_bps, pass_thru)
    if len(jobs) == 0:
        print("0 jobs found matching arguments.")
    else:
        for job_id in sorted(jobs):
            results = service.cancel(job_id, pass_thru)
            if results[0]:
                print(f"Successfully canceled: {job_id}")
            else:
                print(f"Couldn't cancel job with id = {job_id} ({results[1]})")
