//  This file was automatically generated and should not be edited.

import AWSAppSync

public final class ArtworkQuery: GraphQLQuery {
  public static let operationString =
    "query Artwork($artist: String!, $track: String!) {\n  artwork(artist: $artist, track: $track) {\n    __typename\n    artist\n    track\n    url\n  }\n}"

  public var artist: String
  public var track: String

  public init(artist: String, track: String) {
    self.artist = artist
    self.track = track
  }

  public var variables: GraphQLMap? {
    return ["artist": artist, "track": track]
  }

  public struct Data: GraphQLSelectionSet {
    public static let possibleTypes = ["Query"]

    public static let selections: [GraphQLSelection] = [
      GraphQLField("artwork", arguments: ["artist": GraphQLVariable("artist"), "track": GraphQLVariable("track")], type: .object(Artwork.selections)),
    ]

    public var snapshot: Snapshot

    public init(snapshot: Snapshot) {
      self.snapshot = snapshot
    }

    public init(artwork: Artwork? = nil) {
      self.init(snapshot: ["__typename": "Query", "artwork": artwork.flatMap { $0.snapshot }])
    }

    /// Get an artist / track artwork URL
    public var artwork: Artwork? {
      get {
        return (snapshot["artwork"] as? Snapshot).flatMap { Artwork(snapshot: $0) }
      }
      set {
        snapshot.updateValue(newValue?.snapshot, forKey: "artwork")
      }
    }

    public struct Artwork: GraphQLSelectionSet {
      public static let possibleTypes = ["Artwork"]

      public static let selections: [GraphQLSelection] = [
        GraphQLField("__typename", type: .nonNull(.scalar(String.self))),
        GraphQLField("artist", type: .nonNull(.scalar(String.self))),
        GraphQLField("track", type: .nonNull(.scalar(String.self))),
        GraphQLField("url", type: .scalar(String.self)),
      ]

      public var snapshot: Snapshot

      public init(snapshot: Snapshot) {
        self.snapshot = snapshot
      }

      public init(artist: String, track: String, url: String? = nil) {
        self.init(snapshot: ["__typename": "Artwork", "artist": artist, "track": track, "url": url])
      }

      public var __typename: String {
        get {
          return snapshot["__typename"]! as! String
        }
        set {
          snapshot.updateValue(newValue, forKey: "__typename")
        }
      }

      public var artist: String {
        get {
          return snapshot["artist"]! as! String
        }
        set {
          snapshot.updateValue(newValue, forKey: "artist")
        }
      }

      public var track: String {
        get {
          return snapshot["track"]! as! String
        }
        set {
          snapshot.updateValue(newValue, forKey: "track")
        }
      }

      public var url: String? {
        get {
          return snapshot["url"] as? String
        }
        set {
          snapshot.updateValue(newValue, forKey: "url")
        }
      }
    }
  }
}

public final class StationQuery: GraphQLQuery {
  public static let operationString =
    "query Station {\n  station {\n    __typename\n    name\n    streamURL\n    imageURL\n    desc\n    longDesc\n    websiteURL\n    donationURL\n  }\n}"

  public init() {
  }

  public struct Data: GraphQLSelectionSet {
    public static let possibleTypes = ["Query"]

    public static let selections: [GraphQLSelection] = [
      GraphQLField("station", type: .object(Station.selections)),
    ]

    public var snapshot: Snapshot

    public init(snapshot: Snapshot) {
      self.snapshot = snapshot
    }

    public init(station: Station? = nil) {
      self.init(snapshot: ["__typename": "Query", "station": station.flatMap { $0.snapshot }])
    }

    public var station: Station? {
      get {
        return (snapshot["station"] as? Snapshot).flatMap { Station(snapshot: $0) }
      }
      set {
        snapshot.updateValue(newValue?.snapshot, forKey: "station")
      }
    }

    public struct Station: GraphQLSelectionSet {
      public static let possibleTypes = ["Station"]

      public static let selections: [GraphQLSelection] = [
        GraphQLField("__typename", type: .nonNull(.scalar(String.self))),
        GraphQLField("name", type: .nonNull(.scalar(String.self))),
        GraphQLField("streamURL", type: .nonNull(.scalar(String.self))),
        GraphQLField("imageURL", type: .nonNull(.scalar(String.self))),
        GraphQLField("desc", type: .nonNull(.scalar(String.self))),
        GraphQLField("longDesc", type: .nonNull(.scalar(String.self))),
        GraphQLField("websiteURL", type: .nonNull(.scalar(String.self))),
        GraphQLField("donationURL", type: .nonNull(.scalar(String.self))),
      ]

      public var snapshot: Snapshot

      public init(snapshot: Snapshot) {
        self.snapshot = snapshot
      }

      public init(name: String, streamUrl: String, imageUrl: String, desc: String, longDesc: String, websiteUrl: String, donationUrl: String) {
        self.init(snapshot: ["__typename": "Station", "name": name, "streamURL": streamUrl, "imageURL": imageUrl, "desc": desc, "longDesc": longDesc, "websiteURL": websiteUrl, "donationURL": donationUrl])
      }

      public var __typename: String {
        get {
          return snapshot["__typename"]! as! String
        }
        set {
          snapshot.updateValue(newValue, forKey: "__typename")
        }
      }

      public var name: String {
        get {
          return snapshot["name"]! as! String
        }
        set {
          snapshot.updateValue(newValue, forKey: "name")
        }
      }

      public var streamUrl: String {
        get {
          return snapshot["streamURL"]! as! String
        }
        set {
          snapshot.updateValue(newValue, forKey: "streamURL")
        }
      }

      public var imageUrl: String {
        get {
          return snapshot["imageURL"]! as! String
        }
        set {
          snapshot.updateValue(newValue, forKey: "imageURL")
        }
      }

      public var desc: String {
        get {
          return snapshot["desc"]! as! String
        }
        set {
          snapshot.updateValue(newValue, forKey: "desc")
        }
      }

      public var longDesc: String {
        get {
          return snapshot["longDesc"]! as! String
        }
        set {
          snapshot.updateValue(newValue, forKey: "longDesc")
        }
      }

      public var websiteUrl: String {
        get {
          return snapshot["websiteURL"]! as! String
        }
        set {
          snapshot.updateValue(newValue, forKey: "websiteURL")
        }
      }

      public var donationUrl: String {
        get {
          return snapshot["donationURL"]! as! String
        }
        set {
          snapshot.updateValue(newValue, forKey: "donationURL")
        }
      }
    }
  }
}