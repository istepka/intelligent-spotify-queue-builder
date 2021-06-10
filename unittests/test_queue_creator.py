from classes.downloader import Downloader
import unittest
from classes import queue_builder, tracks
from classes import downloader as dwnld
from scripts import dataset_creator, setup


class TestDownloaderFunctions(unittest.TestCase):


    def test_dataset_creation(self):
        name = dataset_creator.create_dataset(tracks_per_year=5)
        self.assert(name != '' and name != None)

    def test_queue_builder(self):
        downloader = dwnld.Downloader(setup.get_spotify_username())
        d = tracks.Track(downloader.fetch_single_track_by_name('Sweet child o mine'))
        d.load_additional_song_data(downloader)
        d.save(downloader=downloader)
        print(d)

        qb = queue_builder.QueueBuilder()

        qb.test_classifier()
        neig = qb.find_neigbors(d)
        print(neig)

        #nearest_tracks = downloader.fetch_tracks_by_ids(neig);
        nearest_tracks =  list(map(lambda x: tracks.Track(x), downloader.fetch_tracks_by_ids(neig)['tracks'] ))

        print(f'\nSimilar to - {d}:\n')
        for i in nearest_tracks:
            print(i)
