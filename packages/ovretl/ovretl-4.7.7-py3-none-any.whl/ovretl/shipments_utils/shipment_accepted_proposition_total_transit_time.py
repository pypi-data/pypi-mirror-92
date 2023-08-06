import pandas as pd


def shipments_accepted_proposition_total_transit_time(shipments_all_propositions_df: pd.DataFrame) -> pd.DataFrame:
    active_shipments = shipments_all_propositions_df[
        ~shipments_all_propositions_df["shipment_status"].isin(["finished", "cancelled"])
    ]
    shipments_accepted_proposition_df = active_shipments[
        shipments_all_propositions_df["proposition_status"] == "accepted"
    ]
    shipments_accepted_proposition_df.loc[
        :, ["transit_time_door_to_port", "transit_time_port_to_door", "transit_time"]
    ] = shipments_accepted_proposition_df[
        ["transit_time_door_to_port", "transit_time_port_to_door", "transit_time"]
    ].fillna(
        0
    )
    shipments_accepted_proposition_df.loc[:, "total_transit_time"] = (
        shipments_accepted_proposition_df["transit_time_door_to_port"]
        + shipments_accepted_proposition_df["transit_time"]
        + shipments_accepted_proposition_df["transit_time_port_to_door"]
    )
    return shipments_accepted_proposition_df
