"""Sample pet data and the search/filter logic behind the Adopt page."""
from collections import Counter

# Filter options: value -> label shown in the UI. Order is the display order.
SPECIES = {"dog": "Dogs", "cat": "Cats"}
AGE_GROUPS = {
    "baby": "Baby / Puppy",
    "young": "Young",
    "adult": "Adult",
    "senior": "Senior",
}
SIZES = {
    "small": "Small (0-25 lbs)",
    "medium": "Medium (26-60 lbs)",
    "large": "Large (61-100 lbs)",
}
SORTS = {
    "newest": "Newest Arrival",
    "oldest": "Oldest Arrival",
    "name": "Name (A-Z)",
}

_PHOTO = "https://images.unsplash.com/"

PETS = [
    {
        "slug": "hazel", "name": "Hazel", "species": "dog", "breed": "Spaniel Mix",
        "age": "3 Months", "age_group": "baby", "size": "medium",
        "gender": "Female", "symbol": "♀", "badge": "Puppy", "arrived": "2025-06-02",
        "image": _PHOTO + "photo-1583337130417-3346a1be7dee",
        "bio": "Hazel is a curious, cuddly spaniel mix who loves chasing leaves and "
               "falling asleep in laps. She is house-training and will thrive with an active family.",
    },
    {
        "slug": "winston", "name": "Winston", "species": "cat", "breed": "British Shorthair",
        "age": "4 Years", "age_group": "adult", "size": "medium",
        "gender": "Male", "symbol": "♂", "badge": "Adult", "arrived": "2025-05-20",
        "image": _PHOTO + "photo-1513360371669-4adf3dd7dff8",
        "bio": "Winston is a calm, dignified gentleman who enjoys sunny windowsills and "
               "quiet evenings. He would suit a relaxed home.",
    },
    {
        "slug": "charlie", "name": "Charlie", "species": "dog", "breed": "Labrador Retriever",
        "age": "6 Years", "age_group": "adult", "size": "large",
        "gender": "Male", "symbol": "♂", "badge": "Special Needs", "highlight": True,
        "arrived": "2025-05-11",
        "image": _PHOTO + "photo-1544568100-847a948585b9",
        "bio": "Charlie is a gentle giant with a slight limp and a huge heart. He needs a "
               "patient family who can help with his daily joint medication.",
    },
    {
        "slug": "luna", "name": "Luna", "species": "cat", "breed": "Domestic Shorthair",
        "age": "1 Year", "age_group": "young", "size": "small",
        "gender": "Female", "symbol": "♀", "arrived": "2025-05-03",
        "image": _PHOTO + "photo-1514888286974-6c03e2ca1dba",
        "bio": "Luna is playful and chatty, with a talent for finding the highest shelf in any room.",
    },
    {
        "slug": "barnaby", "name": "Barnaby", "species": "dog", "breed": "Beagle",
        "age": "9 Years", "age_group": "senior", "size": "medium",
        "gender": "Male", "symbol": "♂", "badge": "Senior", "arrived": "2025-04-22",
        "image": _PHOTO + "photo-1707298737261-069e2d529eaa",
        "bio": "Barnaby is a mellow senior who loves slow sniffy walks and a warm bed. "
               "He is ready to enjoy his golden years in a loving home.",
    },
    {
        "slug": "milo-otis", "name": "Milo & Otis", "species": "cat", "breed": "Orange Tabbies",
        "age": "2 Years", "age_group": "young", "size": "small",
        "gender": "Two males", "symbol": "♂♂", "badge": "Bonded Pair", "highlight": True,
        "arrived": "2025-04-10",
        "image": _PHOTO + "photo-1573865526739-10659fec78a5",
        "bio": "Milo and Otis are inseparable brothers who groom, nap and play together. "
               "They must be adopted as a pair.",
    },
    {
        "slug": "daisy", "name": "Daisy", "species": "dog", "breed": "Golden Retriever",
        "age": "3 Years", "age_group": "young", "size": "large",
        "gender": "Female", "symbol": "♀", "arrived": "2025-03-28",
        "image": _PHOTO + "photo-1543466835-00a7907e9de1",
        "bio": "Daisy is friendly with everyone she meets and already knows her basic commands. "
               "She loves fetch and swimming.",
    },
    {
        "slug": "sylvester", "name": "Sylvester", "species": "cat", "breed": "Tuxedo Cat",
        "age": "5 Years", "age_group": "adult", "size": "medium",
        "gender": "Male", "symbol": "♂", "arrived": "2025-03-15",
        "image": _PHOTO + "photo-1511044568932-338cba0ad803",
        "bio": "Sylvester is a smart, affectionate tuxedo cat who greets visitors at the door "
               "and is happiest when he has company.",
    },
    {
        "slug": "buster", "name": "Buster", "species": "dog", "breed": "Terrier Mix",
        "age": "6 Months", "age_group": "baby", "size": "small",
        "gender": "Male", "symbol": "♂", "badge": "Puppy", "arrived": "2025-03-01",
        "image": _PHOTO + "photo-1548199973-03cce0bbc87b",
        "bio": "Buster is a bundle of terrier energy who is still learning his manners. "
               "He needs an adopter who enjoys training and play.",
    },
]

_BY_SLUG = {pet["slug"]: pet for pet in PETS}


def image_url(pet, width=800):
    """Unsplash URL for a pet photo, resized to `width` pixels."""
    return f"{pet['image']}?w={width}&auto=format&fit=crop"


def get_pet(slug):
    """Return the pet with this slug, or None."""
    return _BY_SLUG.get(slug)


def count_by(field):
    """Count all pets per value of `field`, e.g. count_by("species")."""
    return Counter(pet[field] for pet in PETS)


def search_pets(species=(), age_group=(), size=(), sort="newest"):
    """Filter pets and sort them.

    Each filter is a collection of accepted values. An empty filter matches
    everything; different filters are combined with AND.
    """
    def matches(pet):
        return (
            (not species or pet["species"] in species)
            and (not age_group or pet["age_group"] in age_group)
            and (not size or pet["size"] in size)
        )

    results = [pet for pet in PETS if matches(pet)]
    if sort == "name":
        return sorted(results, key=lambda pet: pet["name"].lower())
    return sorted(results, key=lambda pet: pet["arrived"], reverse=(sort != "oldest"))
