from fastapi import APIRouter, Depends

from app.core.Auth import Permission
from app.core.Response import ListResponseDto, ResponseDto
from app.curd.http.catalog import CatalogDao
from app.curd.http.plan import PlanDao, PlanDetailDao
from app.curd.http.testcase import TestcaseDao
from app.schema.http.plan.plan_in import PlanCreateBody, PlanUpdateBody
from app.utils.utils import ComputerUtils

router = APIRouter(prefix="/plan")


@router.get("/list")
async def list_plan(project_id: int, status="", search="", page: int = 1, limit: int = 10,
                    user_info=Depends(Permission())):
    total, plans = await PlanDao.list(project_id, status, search, page, limit)
    total_page = ComputerUtils.get_total_page(total, limit)
    paging = dict(page=page, limit=limit, total=total, total_page=total_page)
    return ListResponseDto(paging=paging, data=plans)


@router.post("/create")
async def create_plan(plan: PlanCreateBody, user_info=Depends(Permission())):
    await PlanDao.create(plan)
    return ResponseDto(msg="创建成功")


@router.put("/update")
async def update_plan(plan: PlanUpdateBody, user_info=Depends(Permission())):
    await PlanDao.update(plan)
    return ResponseDto(msg="更新成功")


@router.delete("/delete/{pk}")
async def delete_plan(pk: int, user_info=Depends(Permission())):
    await PlanDao.delete(pk=pk)
    return ResponseDto(msg="删除成功")


@router.get("/detail/catalog/tree")
async def get_plan_detail_tree(plan_id: int):
    details = await PlanDetailDao.list_all(plan_id)
    testcase_ids = [detail.testcase_id for detail in details]
    testcases = await TestcaseDao.list_all_by_ids(testcase_ids)
    catalog_ids = [testcase.catalog_id for testcase in testcases]
    tree = await CatalogDao.get_catalog_tree_with_ids(catalog_ids)
    return ResponseDto(data=tree)


@router.get("/detail/testcase/list")
async def list_plan_detail_testcase(plan_id: int, catalog_id="", page: int = 1, limit: int = 10):
    details = await PlanDetailDao.list_all(plan_id)
    testcase_ids = [detail.testcase_id for detail in details]
    total, testcases = await TestcaseDao.list_by_ids_with_condition(testcase_ids, catalog_id)
    total_page = ComputerUtils.get_total_page(total, limit)
    paging = dict(page=page, limit=limit, total=total, total_page=total_page)
    return ListResponseDto(paging=paging, data=testcases)
