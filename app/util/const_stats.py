
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from db import Base
from db import ENGINE
from model import ConstructionTable, ConstructionStatTable, LotTable, LotPriceTable


from collections import defaultdict


def create_construction_stats():
    Session = sessionmaker(bind=ENGINE)
    session = Session()

    construction_stats = []

    constructions = session.query(ConstructionTable).all()
    for construction in constructions:
        # calculate average land area for each construction
        avg_land_area = session.query(func.avg(LotTable.land_area)).filter(
            LotTable.construction_id == construction.id).scalar()

        # calculate frequency counts for categorical fields
        purpose_area_1_counts = defaultdict(int)
        purpose_area_2_counts = defaultdict(int)
        land_use_situation_counts = defaultdict(int)
        topography_height_counts = defaultdict(int)
        topography_form_counts = defaultdict(int)
        road_side_type_counts = defaultdict(int)
        lots = session.query(LotTable).filter(
            LotTable.construction_id == construction.id).all()
        for lot in lots:
            purpose_area_1_counts[lot.purpose_area_1] += 1
            purpose_area_2_counts[lot.purpose_area_2] += 1
            land_use_situation_counts[lot.land_use_situation] += 1
            topography_height_counts[lot.topography_height] += 1
            topography_form_counts[lot.topography_form] += 1
            road_side_type_counts[lot.road_side_type] += 1

        # calculate average price per year for each construction
        lot_prices = session.query(
            func.avg(LotPriceTable.price).label('avg_price')
        ).join(LotTable).filter(
            LotTable.construction_id == construction.id
        ).group_by('year').all()

        avg_price_per_year = {
            price.year: price.avg_price for price in lot_prices}

        # create ConstructionStatTable instance with calculated values
        construction_stats.append(ConstructionStatTable(
            construction_id=construction.id,
            construction=construction,
            avg_land_area=avg_land_area,
            freq_purpose_area_1=purpose_area_1_counts,
            freq_purpose_area_2=purpose_area_2_counts,
            freq_land_use_situation=land_use_situation_counts,
            freq_topography_height=topography_height_counts,
            freq_topography_form=topography_form_counts,
            freq_road_side_type=road_side_type_counts,
            cnt_lot=len(lots),
            avg_price_per_year=avg_price_per_year

        ))

    session.add_all(construction_stats)
    session.commit()


def update_stats():
    create_construction_stats()


if __name__ == '__main__':
    create_construction_stats()
