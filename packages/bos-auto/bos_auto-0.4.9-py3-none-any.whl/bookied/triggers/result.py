from .trigger import Trigger
from bookied_sync import comparators
from bookied_sync.bettingmarketgroup import LookupBettingMarketGroup
from bookied_sync.bettingmarketgroupresolve import LookupBettingMarketGroupResolve
from ..log import log
from .. import exceptions


#: Internal score separator
_SCORE_SEPARATOR = "::"


class ResultTrigger(Trigger):
    """ This trigger deals with the results of an event and needs to combine
        information from different incident reports.
    """

    def _trigger(self, args):
        """ Publish results to a BMG and set to ``finish``.
        """
        log.info("Finishing an event by setting it to " "'finished' (with results)...")

        event = self.getEvent()

        event.status_update(
            "finished", scores=[str(self.home_score), str(self.away_score)]
        )

        log.info("Settling betting market groups...")

        self.resolve_bgms(event)

    def resolve_bgms(self, event):
        """ Resolve the BMGs
        """
        for bmg in event.bettingmarketgroups:
            uialist = list()
            uialist = bmg["asset"]
            name = bmg["description"]["en"]
            x = 0 
            while x < len(uialist):
                bmg["asset"] =  uialist[x]
                if(len(uialist) > 1):
                   bmg["description"]["en"] = name + "_" + str(bmg["asset"]) 
                 
                x += 1
                if bmg["dynamic"]:
                    # Update and crate BMs
                    fuzzy_args = {
                        "test_operation_equal_search": [
                            comparators.cmp_event(),
                            comparators.cmp_description("_dynamic"),
                        ],
                        "find_id_search": [
                            comparators.cmp_event(),
                            comparators.cmp_description("_dynamic"),
                        ],
                    }
                else:
                    fuzzy_args = {}

                # Let's try find an id with fuzzy
                # This also sets the dynamic parameters in the bmg object!
                _ = bmg.find_id(**fuzzy_args)

                # Skip those bmgs that coudn't be found
                if not bmg.find_id():
                    log.error("BMG could not be found: {}".format(str(bmg.identifier)))
                    continue

                settle = LookupBettingMarketGroupResolve(
                    bmg, [self.home_score, self.away_score]
                )
                settle.update()

    def testThreshold(self):
        """ The threshold that needs to be crossed in order to "grade" an event
            on chain (send out the results).

            .. alert:: This is temporary set to be ``2`` until we have an
                easier way to identify how many data proxies send data to us
        """
        return 2

    def testThresholdPercentage(self):
        """ This is the percentage of incidents that needs to agree on the
            results before we push them on-chain
        """
        return 51

    def _count_score(self, scores):
        """ Internal counter of scores
        """
        from collections import Counter

        ret = Counter()
        for i in range(len(scores)):
            ret[scores[i]] += 1
        return ret

    def testConditions(self, *args, **kwargs):
        """ The test conditions for "grading" the event are as this:

            * Raise if less than ``testThreshold`` result incidents received
            * Raise if less than ``testThresholdPercentage`` result incidents agree on the result
            * Raise if multiple results reach above thresholds
            * Else, publish the result that is left

        """
        incidents = self.get_all_incidents()
        if not incidents:
            raise exceptions.InsufficientIncidents
        result_incidents = incidents.get("result", {}).get("incidents", [])
        if not result_incidents:
            raise exceptions.InsufficientIncidents
        provider_hashes = set()
        for incident in result_incidents:
            provider_hash = incident.get("provider_info", {}).get("name", None)
            if provider_hash is not None:
                provider_hashes.add(provider_hash)
        if len(provider_hashes) < self.testThreshold():
            log.info(
                "Insufficient incidents for {}({})".format(
                    self.__class__.__name__, str(self.teams)
                )
            )
            raise exceptions.InsufficientIncidents

        # Figure out the most "probable" result
        scores = [
            "{}{}{}".format(
                x["arguments"]["away_score"],
                _SCORE_SEPARATOR,
                x["arguments"]["home_score"],
            )
            for x in result_incidents
        ]
        scores = self._count_score(scores)

        # Threshold scaled by number of scores
        threshold = len(scores) * self.testThresholdPercentage() / 100

        # Valid results filtered by threshold
        valid_results = dict({k: v for k, v in scores.items() if v >= threshold})

        # Raise if multiple results are valid
        if len(valid_results) > 1:
            log.info("Too many different results over threshold")
            raise exceptions.TooManyDifferentResultsOverThreshold(valid_results)
        elif not valid_results:
            log.info("Insufficient Equal Results")
            raise exceptions.InsufficientEqualResults
        else:
            result = list(valid_results.keys())[0]
            self.away_score, self.home_score = result.split(_SCORE_SEPARATOR)
            log.info(
                "Resolving: home - away: ({} - {})".format(
                    self.home_score, self.away_score
                )
            )
            return True
