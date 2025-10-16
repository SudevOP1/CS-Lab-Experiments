const uniData = {
  unis: [
    {
      name: "University of Oxford",
      marksExpected: {
        ssc: {
          min: 85,
          max: 95,
        },
        hsc: {
          min: 90,
          max: 98,
        },
        sem1: {
          min: 80,
          max: 95,
        },
        sem2: {
          min: 82,
          max: 97,
        },
        sem3: {
          min: 83,
          max: 96,
        },
        sem4: {
          min: 84,
          max: 98,
        },
        sem5: {
          min: 85,
          max: 99,
        },
        sem6: {
          min: 86,
          max: 100,
        },
        sem7: {
          min: 87,
          max: 100,
        },
        sem8: {
          min: 88,
          max: 100,
        },
      },
    },
    {
      name: "Harvard University",
      marksExpected: {
        ssc: {
          min: 85,
          max: 100,
        },
        hsc: {
          min: 88,
          max: 99,
        },
        sem1: {
          min: 85,
          max: 95,
        },
        sem2: {
          min: 87,
          max: 98,
        },
        sem3: {
          min: 89,
          max: 97,
        },
        sem4: {
          min: 90,
          max: 99,
        },
        sem5: {
          min: 91,
          max: 100,
        },
        sem6: {
          min: 92,
          max: 100,
        },
        sem7: {
          min: 94,
          max: 100,
        },
        sem8: {
          min: 95,
          max: 100,
        },
      },
    },
    {
      name: "University of Melbourne",
      marksExpected: {
        ssc: {
          min: 80,
          max: 90,
        },
        hsc: {
          min: 85,
          max: 95,
        },
        sem1: {
          min: 75,
          max: 90,
        },
        sem2: {
          min: 77,
          max: 91,
        },
        sem3: {
          min: 79,
          max: 93,
        },
        sem4: {
          min: 80,
          max: 94,
        },
        sem5: {
          min: 82,
          max: 96,
        },
        sem6: {
          min: 84,
          max: 97,
        },
        sem7: {
          min: 85,
          max: 98,
        },
        sem8: {
          min: 87,
          max: 100,
        },
      },
    },
    {
      name: "ETH Zurich",
      marksExpected: {
        ssc: {
          min: 85,
          max: 100,
        },
        hsc: {
          min: 88,
          max: 98,
        },
        sem1: {
          min: 85,
          max: 95,
        },
        sem2: {
          min: 86,
          max: 97,
        },
        sem3: {
          min: 87,
          max: 98,
        },
        sem4: {
          min: 88,
          max: 99,
        },
        sem5: {
          min: 89,
          max: 100,
        },
        sem6: {
          min: 90,
          max: 100,
        },
        sem7: {
          min: 91,
          max: 100,
        },
        sem8: {
          min: 92,
          max: 100,
        },
      },
    },
    {
      name: "National University of Singapore",
      marksExpected: {
        ssc: {
          min: 80,
          max: 90,
        },
        hsc: {
          min: 85,
          max: 95,
        },
        sem1: {
          min: 80,
          max: 90,
        },
        sem2: {
          min: 82,
          max: 91,
        },
        sem3: {
          min: 83,
          max: 92,
        },
        sem4: {
          min: 85,
          max: 93,
        },
        sem5: {
          min: 86,
          max: 94,
        },
        sem6: {
          min: 87,
          max: 95,
        },
        sem7: {
          min: 89,
          max: 96,
        },
        sem8: {
          min: 90,
          max: 97,
        },
      },
    },
  ],
};

export function getUniData(uniName) {
  if (uniName) {
    for (let uni of uniData.unis) {
      if (uni.name === uniName) {
        return uni;
      }
    }
  }
  return null;
}

export function getAvailableUnis() {
  return uniData.unis.map((uni) => uni.name);
}
