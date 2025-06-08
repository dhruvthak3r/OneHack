from utils import split_and_format_date,read_json_file

from models.schemas import HackathonSchema


def transform_devpost(filename):
    data = read_json_file(filename)

    result = []
    for hackathon_container in data:  # Proper indentation
        for hackathons in hackathon_container["hackathons"]:
            starts_at, ends_at = split_and_format_date(hackathons["submission_period_dates"])
            devpost_hackathons = HackathonSchema(
                name=hackathons["title"],
                link=hackathons["url"],
                starts_at=starts_at,
                ends_at=ends_at,
                reg_starts_at=starts_at,
                reg_ends_at=ends_at,
                mode="online" if hackathons["displayed_location"]["location"] == "Online" else "offline",
                platform="Devpost"
            )
            result.append(devpost_hackathons.model_dump())
    return result  



if __name__ == "__main__":
    filename = "devpost_hackathons.json"
    transformed_data = transform_devpost(filename)
    print(transformed_data)
